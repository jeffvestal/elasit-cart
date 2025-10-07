import { NextRequest, NextResponse } from 'next/server';

// Agent chat endpoint to proxy requests to Agent Builder
export async function POST(request: NextRequest) {
  try {
    const { message, agentId, sessionId } = await request.json();

    // Validate required fields
    if (!message || !agentId) {
      return NextResponse.json(
        { 
          success: false, 
          message: 'Message and agent ID are required' 
        },
        { status: 400 }
      );
    }

    // Get environment variables
    const kibanaUrl = process.env.KIBANA_URL;
    const kibanaApiKey = process.env.KIBANA_API_KEY;

    if (!kibanaUrl || !kibanaApiKey) {
      console.error('❌ Missing KIBANA_URL or KIBANA_API_KEY environment variables');
      return NextResponse.json(
        { 
          success: false, 
          message: 'Agent Builder not configured' 
        },
        { status: 500 }
      );
    }

    console.log(`🤖 Agent chat request: ${agentId} - "${message.substring(0, 50)}..."`);

    // Map frontend agent IDs to backend agent IDs
    const agentIdMapping: Record<string, string> = {
      'budget_master': 'budget_master',
      'health_guru': 'health_guru', 
      'gourmet_chef': 'gourmet_chef',
      'speed_shopper': 'speed_shopper',
      'vegas_local': 'local_expert' // Map vegas_local to local_expert
    };
    
    const backendAgentId = agentIdMapping[agentId] || agentId;
    console.log(`🔄 Agent ID mapping: ${agentId} -> ${backendAgentId}`);

    // Prepare the request to Agent Builder
    const agentBuilderUrl = `${kibanaUrl.replace(/\/$/, '')}/api/agent_builder/converse`;
    
    const chatPayload = {
      input: message,
      agent_id: backendAgentId
    };

    console.log(`🔗 Agent Builder URL: ${agentBuilderUrl}`);
    console.log(`📦 Payload:`, JSON.stringify(chatPayload, null, 2));

    // Make request to Agent Builder
    const response = await fetch(agentBuilderUrl, {
      method: 'POST',
      headers: {
        'Authorization': `ApiKey ${kibanaApiKey}`,
        'Content-Type': 'application/json',
        'kbn-xsrf': 'true'
      },
      body: JSON.stringify(chatPayload)
    });

    console.log(`📡 Response status: ${response.status}`);

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`❌ Agent Builder API error: ${response.status} - ${errorText}`);
      
      // Return a fallback response for demo purposes
      return NextResponse.json({
        success: true,
        response: `I'm having trouble connecting to the Agent Builder right now. This is a demo response for agent ${agentId}. In a real scenario, I would help you find grocery items based on your request: "${message}"`,
        items: [], // No suggested items for fallback
        agentId,
        sessionId: sessionId || `fallback_${Date.now()}`
      });
    }

    const agentResponse = await response.json();
    console.log(`✅ Agent response received from ${agentId}:`, JSON.stringify(agentResponse, null, 2));

    // Parse the agent response and extract any suggested items
    // The response should contain the agent's message in the 'output' field
    let responseText = agentResponse.output || agentResponse.response?.message || '';
    
    // If the response is empty but we have tool results, create a helpful response
    if (!responseText || responseText.trim() === '') {
      responseText = generateResponseFromToolResults(agentResponse, agentId);
    }
    
    // Try to extract suggested items from the response and tool results
    const suggestedItems = extractSuggestedItemsFromAgentResponse(agentResponse);

    return NextResponse.json({
      success: true,
      response: responseText,
      items: suggestedItems,
      agentId,
      sessionId: agentResponse.session_id || sessionId,
      metadata: {
        timestamp: new Date().toISOString(),
        agentUsed: agentId,
        rawResponse: agentResponse, // Include raw response for debugging
        steps: agentResponse.steps || [] // Include steps for UI display
      }
    });

  } catch (error) {
    console.error('❌ Agent chat error:', error);
    
    // Return a fallback response
    return NextResponse.json({
      success: true,
      response: "I'm experiencing some technical difficulties right now. Please try your request again, or contact support if the problem persists.",
      items: [],
      agentId: request.body?.agentId || 'unknown',
      sessionId: request.body?.sessionId || `error_${Date.now()}`
    });
  }
}

// Helper function to generate response from tool results when agent response is empty
function generateResponseFromToolResults(agentResponse: any, agentId: string): string {
  const steps = agentResponse.steps || [];
  const toolCalls = steps.filter((step: any) => step.type === 'tool_call');
  
  if (toolCalls.length === 0) {
    return `I'm working on your request! Let me search for the best options for you.`;
  }

  const toolCall = toolCalls[0];
  const results = toolCall.results || [];
  const tabularData = results.find((r: any) => r.type === 'tabular_data');
  
  if (!tabularData || !tabularData.data.values || tabularData.data.values.length === 0) {
    return `I searched for items but didn't find any matches. Let me try a different approach for you!`;
  }

  // Get unique items only
  const allItems = tabularData.data.values.filter((item: any) => item && item.length > 0);
  const uniqueItems: any[] = [];
  const seenNames = new Set<string>();
  
  for (const item of allItems) {
    let name: string, brand: string, price: number;
    
    // Handle different data structures
    if (item.length <= 12) {
      // Budget/simple tool structure
      [price, , , , , name, brand] = item;
    } else {
      // Detailed tool structure - find name and brand
      price = parseFloat(item[0]) || 0;
      name = 'Product';
      brand = 'Unknown';
      
      // Find name field
      for (let i = 15; i < Math.min(item.length, 30); i++) {
        const field = item[i];
        if (typeof field === 'string' && 
            field.length > 3 && 
            !field.startsWith('ITEM_') && 
            !field.startsWith('INV_') && 
            !field.includes('T18:36:22') &&
            !field.startsWith('POINT (') &&
            !field.match(/^\d{2}:\d{2}/) &&
            field !== 'Las Vegas' && field !== 'NV') {
          name = field;
          if (i + 1 < item.length && typeof item[i + 1] === 'string') {
            brand = item[i + 1];
          }
          break;
        }
      }
    }
    
    if (!name || !price || price <= 0) continue;
    
    const itemName = name.toString().trim();
    
    if (!seenNames.has(itemName) && uniqueItems.length < 5) {
      seenNames.add(itemName);
      uniqueItems.push({ name, brand, price });
    }
  }
  
  const agentPersonality = getAgentPersonality(agentId);
  
  let response = `${agentPersonality.greeting} I found ${uniqueItems.length} unique options for your 5 bags!\n\n`;
  
  uniqueItems.forEach((item: any, index: number) => {
    response += `${index + 1}. **${item.name}** (${item.brand})\n`;
    response += `   💰 $${item.price} | Perfect for bag #${index + 1}!\n\n`;
  });
  
  if (uniqueItems.length < 5) {
    response += `⚠️ I found ${uniqueItems.length} unique items. Let me search for more to fill all 5 bags!\n\n`;
  }
  
  response += `${agentPersonality.closing}`;
  
  return response;
}

// Helper function to extract suggested items from agent response
function extractSuggestedItemsFromAgentResponse(agentResponse: any): any[] {
  const steps = agentResponse.steps || [];
  const toolCalls = steps.filter((step: any) => step.type === 'tool_call');
  const items: any[] = [];
  const seenNames = new Set<string>(); // Track unique item names
  
  toolCalls.forEach((toolCall: any) => {
    const results = toolCall.results || [];
    const tabularData = results.find((r: any) => r.type === 'tabular_data');
    
    if (tabularData && tabularData.data.values) {
      // Process all items but only add unique ones
      tabularData.data.values.forEach((item: any[], index: number) => {
        if (!item || item.length === 0) return; // Skip null/empty items
        
        let bestPrice: number, itemId: string, name: string, brand: string, category: string;
        
        // Handle different data structures returned by different tools
        if (item.length === 12) {
          // New search_grocery_items structure: [avg_price, min_price, max_price, stores_available, item_id, name, brand, category, unit_size, organic, gluten_free, vegan]
          const [avgPrice, minPrice, maxPrice, storesAvailable, id, itemName, brandName, cat] = item;
          bestPrice = parseFloat(avgPrice.toString()) || 0;
          itemId = id || `item_${index}`;
          name = itemName || `Product ${index + 1}`;
          brand = brandName || 'Unknown Brand';
          category = cat || 'Suggested';
        } else if (item.length <= 11) {
          // Budget/simple tool structure: [best_price, avg_price, stores_count, max_discount_score, item_id, name, brand, category, unit_size, organic, value_score]
          [bestPrice, , , , itemId, name, brand, category] = item;
        } else {
          // Detailed tool structure: [price, inv_id, item_id, timestamp, ...many fields..., name, ...]
          // The name is typically around index 20-21 in the detailed structure
          bestPrice = parseFloat(item[0]) || 0;
          itemId = item[2] || `item_${index}`;

          // Find the name field by looking for string values that look like product names
          // In the detailed structure, name usually appears after the brand field
          let nameIndex = -1;
          let brandIndex = -1;

          // Look for typical product names (not IDs, timestamps, or numbers)
          for (let i = 15; i < Math.min(item.length, 30); i++) {
            const field = item[i];
            if (typeof field === 'string' &&
                field.length > 3 &&
                !field.startsWith('ITEM_') &&
                !field.startsWith('INV_') &&
                !field.startsWith('STORE_') &&
                !field.includes('T18:36:22') && // Not a timestamp
                !field.startsWith('POINT (') && // Not coordinates
                !field.match(/^\d{2}:\d{2}/) && // Not time format
                !field.match(/^\d{3}-\d{3}-\d{4}/) && // Not phone number
                !field.match(/^\d{5}$/) && // Not zip code
                field !== 'true' && field !== 'false' &&
                field !== 'lb' && field !== 'package' && field !== 'oz' &&
                field !== 'Las Vegas' && field !== 'NV') {

              // This looks like a product name or brand
              if (nameIndex === -1) {
                nameIndex = i;
                name = field;
              } else if (brandIndex === -1 && i === nameIndex + 1) {
                brandIndex = i;
                brand = field;
                break;
              }
            }
          }

          // Fallback if we couldn't find proper name/brand
          if (!name) {
            name = `Product ${index + 1}`;
          }
          if (!brand) {
            brand = 'Unknown Brand';
          }

          // Try to find category
          category = 'Suggested';
          for (let i = 0; i < item.length; i++) {
            const field = item[i];
            if (typeof field === 'string' &&
                (field.includes('Meat') || field.includes('Dairy') ||
                 field.includes('Produce') || field.includes('Pantry') ||
                 field.includes('Seafood') || field.includes('Bakery'))) {
              category = field;
              break;
            }
          }
        }
        
        if (!name || !bestPrice || bestPrice <= 0) return; // Skip invalid items
        
        // Now that agents return proper items, only filter out invalid prices
        if (bestPrice < 1) {
          console.log(`Skipping invalid item: ${name} at $${bestPrice}`);
          return; // Skip invalid items only
        }
        
        const itemName = name.toString().trim();
        
        // Only add if we haven't seen this item name before and we have less than 5 items
        if (!seenNames.has(itemName) && items.length < 5) {
          seenNames.add(itemName);
          
          // Try to parse quantity from the response text (look for patterns like "3x", "2 x", etc.)
          let quantity = 1;
          const responseText = agentResponse.output || '';
          
          // Look for quantity patterns in the response - be more flexible
          const quantityPatterns = [
            new RegExp(`(\\d+)\\s*x\\s*.*${itemName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, 'i'),
            new RegExp(`(\\d+)\\s*.*${itemName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}.*each`, 'i'),
            new RegExp(`(\\d+)\\s+${itemName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, 'i'),
            // More flexible patterns
            new RegExp(`(\\d+)\\s*${itemName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`, 'i'),
            new RegExp(`${itemName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}.*?(\\d+)`, 'i')
          ];
          
          for (const pattern of quantityPatterns) {
            const match = responseText.match(pattern);
            if (match && match[1]) {
              const parsedQuantity = parseInt(match[1]);
              if (parsedQuantity > 0 && parsedQuantity <= 20) { // Reasonable quantity limits
                quantity = parsedQuantity;
                break;
              }
            }
          }
          
          // If no quantity found in text, suggest reasonable quantities based on price to reach ~$20 per item
          if (quantity === 1) {
            // Calculate quantity to get item price closer to $15-25 range
            const targetPrice = 20; // Target around $20 per item for $100 total
            const calculatedQuantity = Math.max(1, Math.round(targetPrice / bestPrice));
            quantity = Math.min(calculatedQuantity, 10); // Cap at 10 to be reasonable
            
            console.log(`Auto-calculated quantity for ${name}: ${quantity}x at $${bestPrice} = $${(quantity * bestPrice).toFixed(2)}`);
          }
          
          items.push({
            id: `suggested_${Date.now()}_${Math.random().toString(36).substr(2, 9)}_${items.length}`,
            name: `${itemName} (${brand})`,
            price: parseFloat(bestPrice.toString()), // Ensure it's a number
            store: 'Agent Suggestion',
            category: category || 'Suggested',
            quantity: quantity
          });
        }
      });
    }
  });
  
  return items;
}

// Helper function to get agent personality for responses
function getAgentPersonality(agentId: string): { greeting: string; closing: string } {
  const personalities: Record<string, { greeting: string; closing: string }> = {
    speed_shopper: {
      greeting: "⚡ Speed Shopper here!",
      closing: "These are quick wins that'll get you to $100 fast! Add them to your cart and let's keep moving! 🚀"
    },
    budget_master: {
      greeting: "💰 Budget Master at your service!",
      closing: "These deals will stretch your budget perfectly! Each one is a smart choice for your $100 goal! 💪"
    },
    health_guru: {
      greeting: "🥗 Health Guru here to help!",
      closing: "These nutritious options will fuel your body while staying within budget! Great choices for your wellness journey! 🌟"
    },
    gourmet_chef: {
      greeting: "👨‍🍳 Gourmet Chef ready to inspire!",
      closing: "These ingredients will create amazing meals! Each one brings quality and flavor to your culinary adventures! ✨"
    },
    local_expert: {
      greeting: "🎰 Vegas Local Expert here!",
      closing: "These are some of the best values you'll find in Sin City! Local favorites that won't break the bank! 🎲"
    }
  };
  
  return personalities[agentId] || {
    greeting: "🤖 Agent here to help!",
    closing: "These are great options for your shopping needs!"
  };
}

// Helper function to extract suggested items from text (fallback)
function extractSuggestedItems(responseText: string): any[] {
  const items: any[] = [];
  
  // Look for patterns like "Product Name - $X.XX" or similar
  // This is a basic implementation - you may need to enhance based on your agent response format
  const itemPattern = /([A-Za-z\s]+)\s*-\s*\$(\d+\.\d{2})/g;
  let match;
  
  while ((match = itemPattern.exec(responseText)) !== null) {
    const [, name, price] = match;
    items.push({
      id: `item_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: name.trim(),
      price: parseFloat(price),
      store: 'Agent Suggestion',
      category: 'Suggested',
      quantity: 1
    });
  }
  
  return items;
}

// GET endpoint for testing
export async function GET() {
  return NextResponse.json({
    message: 'Agent chat endpoint is running',
    timestamp: new Date().toISOString(),
    environment: {
      hasKibanaUrl: !!process.env.KIBANA_URL,
      hasKibanaApiKey: !!process.env.KIBANA_API_KEY
    }
  });
}