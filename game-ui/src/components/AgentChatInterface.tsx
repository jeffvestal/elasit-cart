'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Bot, User, Sparkles, MessageCircle, Loader2 } from 'lucide-react';
import { useGameStore } from '@/store/gameStore';
import { Button } from '@/components/ui/Button';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  items?: any[];
}

interface AgentChatInterfaceProps {
  className?: string;
}

export function AgentChatInterface({ className = '' }: AgentChatInterfaceProps) {
  const { selectedAgent, addItem, session, gameStarted, gameEnded } = useGameStore();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message when agent is selected
    if (selectedAgent && messages.length === 0) {
      const welcomeMessage: ChatMessage = {
        id: 'welcome',
        role: 'assistant',
        content: `Hi! I'm ${selectedAgent.name}, your ${selectedAgent.description.toLowerCase()}. I'm here to help you build the perfect $100 grocery cart! 

What kind of items are you looking for today? I can help you find:
• Great deals and discounts
• Items that fit your dietary needs  
• Recipe combinations
• Seasonal specialties
• Store-specific bargains

Just tell me what you have in mind!`,
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    }
  }, [selectedAgent, messages.length]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !selectedAgent || !session) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: inputMessage.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      // Simulate agent response with mock data
      // In real implementation, this would call the Agent Builder API
      const mockResponse = await simulateAgentResponse(inputMessage.trim(), selectedAgent.id);
      
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: mockResponse.message,
        timestamp: new Date(),
        items: mockResponse.items || [],
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Add items to cart if any were suggested
      mockResponse.items?.forEach(item => {
        addItem({
          id: item.id,
          name: item.name,
          price: item.price,
          quantity: item.quantity || 1,
          store: item.store || 'Lucky Strike Market',
          category: item.category || 'General',
        });
      });

    } catch (error) {
      console.error('Error getting agent response:', error);
      
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "I'm sorry, I'm having trouble processing your request right now. Please try again!",
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!selectedAgent) {
    return (
      <div className={`bg-white rounded-2xl shadow-lg border border-gray-200 p-8 ${className}`}>
        <div className="text-center">
          <div className="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <Bot className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Select an Agent</h3>
          <p className="text-gray-500">
            Choose your AI shopping assistant to start chatting and building your cart!
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-2xl shadow-lg border border-gray-200 flex flex-col ${className}`}>
      {/* Header */}
      <div className="p-4 border-b border-gray-200 bg-gradient-to-r from-elastic-blue/5 to-elastic-teal/5">
        <div className="flex items-center space-x-3">
          <div className={`w-10 h-10 ${selectedAgent.color} rounded-full flex items-center justify-center`}>
            <span className="text-white text-lg">{selectedAgent.avatar}</span>
          </div>
          <div className="flex-1">
            <div className="flex items-center space-x-2">
              <h3 className="font-semibold text-gray-900">{selectedAgent.name}</h3>
              <div className="flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
                <span className="text-xs text-green-600 font-medium">Online</span>
              </div>
            </div>
            <p className="text-sm text-gray-600">{selectedAgent.description}</p>
          </div>
          <div className="bg-elastic-blue/10 p-2 rounded-full">
            <MessageCircle className="h-4 w-4 text-elastic-blue" />
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-96">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] ${message.role === 'user' ? 'order-2' : 'order-1'}`}>
                <div className={`rounded-2xl px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-elastic-blue text-white ml-auto'
                    : 'bg-gray-100 text-gray-900'
                }`}>
                  {message.role === 'assistant' && (
                    <div className="flex items-center space-x-2 mb-2">
                      <span className="text-lg">{selectedAgent.avatar}</span>
                      <span className="text-xs font-medium text-gray-600">
                        {selectedAgent.name}
                      </span>
                    </div>
                  )}
                  
                  <div className="whitespace-pre-wrap text-sm leading-relaxed">
                    {message.content}
                  </div>

                  {/* Show suggested items */}
                  {message.items && message.items.length > 0 && (
                    <div className="mt-3 space-y-2">
                      <div className="text-xs font-medium text-gray-600 flex items-center">
                        <Sparkles className="h-3 w-3 mr-1" />
                        Suggested Items:
                      </div>
                      {message.items.map((item, idx) => (
                        <div key={idx} className="bg-white rounded-lg p-2 border border-gray-200">
                          <div className="flex items-center justify-between">
                            <div>
                              <div className="font-medium text-xs text-gray-900">{item.name}</div>
                              <div className="text-xs text-gray-500">{item.store}</div>
                            </div>
                            <div className="text-elastic-blue font-semibold text-sm">
                              ${item.price.toFixed(2)}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  <div className="text-xs opacity-70 mt-2">
                    {message.timestamp.toLocaleTimeString([], { 
                      hour: '2-digit', 
                      minute: '2-digit' 
                    })}
                  </div>
                </div>
              </div>

              <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                message.role === 'user' 
                  ? 'bg-elastic-blue ml-2 order-1' 
                  : 'bg-gray-200 mr-2 order-2'
              }`}>
                {message.role === 'user' ? (
                  <User className="h-4 w-4 text-white" />
                ) : (
                  <span className="text-sm">{selectedAgent.avatar}</span>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="flex justify-start"
          >
            <div className="bg-gray-100 rounded-2xl px-4 py-3 max-w-[80%]">
              <div className="flex items-center space-x-2">
                <span className="text-lg">{selectedAgent.avatar}</span>
                <Loader2 className="h-4 w-4 animate-spin text-gray-500" />
                <span className="text-sm text-gray-600">Thinking...</span>
              </div>
            </div>
          </motion.div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        {gameEnded ? (
          <div className="text-center py-4">
            <div className="text-sm text-gray-500 mb-2">🎉 Game completed!</div>
            <div className="text-xs text-gray-400">
              Chat is now disabled. Thanks for playing!
            </div>
          </div>
        ) : !gameStarted ? (
          <div className="text-center py-4">
            <div className="text-sm text-gray-500 mb-2">Ready to start shopping?</div>
            <div className="text-xs text-gray-400">
              Start the game to begin chatting with your agent!
            </div>
          </div>
        ) : (
          <div className="flex space-x-2">
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={`Ask ${selectedAgent.name} for help...`}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-elastic-blue focus:border-transparent resize-none"
              disabled={isLoading}
            />
            <Button
              onClick={handleSendMessage}
              disabled={!inputMessage.trim() || isLoading}
              variant="elastic"
              size="md"
              className="px-4"
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        )}
      </div>
    </div>
  );
}

// Mock function to simulate agent responses
// In real implementation, this would call the Agent Builder API
async function simulateAgentResponse(message: string, agentId: string) {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));

  const mockItems = [
    { id: '1', name: 'Organic Bananas', price: 2.99, store: 'Lucky Strike Market', category: 'Fresh Produce' },
    { id: '2', name: 'Ground Turkey', price: 6.49, store: 'Jackpot Grocers', category: 'Meat & Seafood' },
    { id: '3', name: 'Greek Yogurt', price: 5.99, store: 'All-In Foods', category: 'Dairy & Eggs' },
    { id: '4', name: 'Whole Grain Bread', price: 3.49, store: 'Lucky Strike Market', category: 'Bakery' },
    { id: '5', name: 'Olive Oil', price: 8.99, store: 'High Roller Gourmet', category: 'Pantry Staples' },
  ];

  // Simple keyword matching for demo
  const keywords = message.toLowerCase();
  let selectedItems: any[] = [];
  let responseMessage = '';

  if (keywords.includes('healthy') || keywords.includes('nutrition')) {
    selectedItems = [mockItems[0], mockItems[2], mockItems[3]];
    responseMessage = `Great choice focusing on healthy options! I found some nutritious items that fit perfectly within your budget. These organic bananas are packed with potassium, the Greek yogurt provides protein, and whole grain bread gives you fiber. Total for these items: $${selectedItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}`;
  } else if (keywords.includes('cheap') || keywords.includes('budget') || keywords.includes('deal')) {
    selectedItems = [mockItems[1], mockItems[3]];
    responseMessage = `I found some great budget-friendly options! The ground turkey is on sale at Jackpot Grocers, and this whole grain bread is both nutritious and affordable. These items give you great value for money. Total: $${selectedItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}`;
  } else if (keywords.includes('cook') || keywords.includes('recipe') || keywords.includes('meal')) {
    selectedItems = [mockItems[1], mockItems[4], mockItems[3]];
    responseMessage = `Perfect for cooking! I've selected items that work beautifully together. You can make delicious turkey meatballs with this ground turkey, use the premium olive oil for cooking, and serve with toasted whole grain bread. These ingredients are versatile and will create multiple meals. Total: $${selectedItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}`;
  } else {
    selectedItems = [mockItems[0], mockItems[2]];
    responseMessage = `I found some great items based on your request! These organic bananas are perfect for snacking or smoothies, and the Greek yogurt is versatile - great for breakfast, snacks, or cooking. Both are from highly-rated stores in Vegas. Total: $${selectedItems.reduce((sum, item) => sum + item.price, 0).toFixed(2)}`;
  }

  return {
    message: responseMessage,
    items: selectedItems,
  };
}
