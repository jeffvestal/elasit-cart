'use client';

import { motion } from 'framer-motion';
import { ShoppingCart, Trash2, Plus, Minus, DollarSign, Package } from 'lucide-react';
import { useGameStore, GameItem } from '@/store/gameStore';
import { Button } from '@/components/ui/Button';

interface ShoppingCartProps {
  className?: string;
}

export function ShoppingCart({ className = '' }: ShoppingCartProps) {
  const { 
    currentItems, 
    removeItem, 
    updateItemQuantity,
    session
  } = useGameStore();

  const totalPrice = currentItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const targetPrice = session?.targetPrice || 100;
  const remainingBudget = targetPrice - totalPrice;
  const isOverBudget = totalPrice > targetPrice;

  const handleQuantityChange = (itemId: string, change: number) => {
    const item = currentItems.find(i => i.id === itemId);
    if (item) {
      const newQuantity = Math.max(0, item.quantity + change);
      updateItemQuantity(itemId, newQuantity);
    }
  };

  if (currentItems.length === 0) {
    return (
      <div className={`bg-white rounded-2xl shadow-lg border border-gray-200 p-6 ${className}`}>
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="bg-elastic-blue p-2 rounded-full">
              <ShoppingCart className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Shopping Cart</h3>
              <p className="text-sm text-gray-500">Build your $100 cart</p>
            </div>
          </div>
        </div>

        <div className="text-center py-12">
          <div className="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <Package className="h-8 w-8 text-gray-400" />
          </div>
          <h4 className="text-gray-900 font-medium mb-2">Cart is Empty</h4>
          <p className="text-gray-500 text-sm">
            Chat with your agent to start adding items!
          </p>
        </div>

        {/* Budget Display */}
        <div className="bg-gradient-to-r from-elastic-blue/10 to-elastic-teal/10 rounded-xl p-4 border border-elastic-blue/20">
          <div className="flex items-center justify-between">
            <span className="text-gray-700 font-medium">Target:</span>
            <span className="text-2xl font-bold text-elastic-blue">
              ${targetPrice.toFixed(2)}
            </span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-2xl shadow-lg border border-gray-200 ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-elastic-blue p-2 rounded-full">
              <ShoppingCart className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Shopping Cart</h3>
              <p className="text-sm text-gray-500">{currentItems.length} items</p>
            </div>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-500">Current Total</div>
            <div className={`text-2xl font-bold ${isOverBudget ? 'text-red-600' : 'text-elastic-blue'}`}>
              ${totalPrice.toFixed(2)}
            </div>
          </div>
        </div>
      </div>

      {/* Items List */}
      <div className="max-h-96 overflow-y-auto">
        {currentItems.map((item, index) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className="p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-start space-x-3">
              {/* Item Info */}
              <div className="flex-1 min-w-0">
                <h4 className="font-medium text-gray-900 truncate">{item.name}</h4>
                <div className="flex items-center space-x-2 text-sm text-gray-500 mt-1">
                  <span>{item.category}</span>
                  <span>•</span>
                  <span>{item.store}</span>
                </div>
                <div className="flex items-center space-x-2 mt-2">
                  <span className="text-lg font-semibold text-elastic-blue">
                    ${item.price.toFixed(2)}
                  </span>
                  <span className="text-sm text-gray-500">each</span>
                </div>
              </div>

              {/* Quantity Controls */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleQuantityChange(item.id, -1)}
                  className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors"
                >
                  <Minus className="h-4 w-4 text-gray-600" />
                </button>
                
                <div className="w-12 text-center">
                  <span className="font-medium text-gray-900">{item.quantity}</span>
                </div>
                
                <button
                  onClick={() => handleQuantityChange(item.id, 1)}
                  className="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 flex items-center justify-center transition-colors"
                >
                  <Plus className="h-4 w-4 text-gray-600" />
                </button>
              </div>

              {/* Item Total & Remove */}
              <div className="flex items-center space-x-3">
                <div className="text-right">
                  <div className="font-semibold text-gray-900">
                    ${(item.price * item.quantity).toFixed(2)}
                  </div>
                </div>
                
                <button
                  onClick={() => removeItem(item.id)}
                  className="w-8 h-8 rounded-full bg-red-100 hover:bg-red-200 flex items-center justify-center transition-colors group"
                >
                  <Trash2 className="h-4 w-4 text-red-600 group-hover:text-red-700" />
                </button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Footer with Totals */}
      <div className="p-6 border-t border-gray-200 space-y-4">
        {/* Budget Status */}
        <div className={`rounded-xl p-4 ${
          isOverBudget 
            ? 'bg-red-50 border border-red-200' 
            : remainingBudget < 10 
              ? 'bg-yellow-50 border border-yellow-200'
              : 'bg-green-50 border border-green-200'
        }`}>
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center space-x-2">
                <DollarSign className={`h-5 w-5 ${
                  isOverBudget ? 'text-red-600' : remainingBudget < 10 ? 'text-yellow-600' : 'text-green-600'
                }`} />
                <span className="font-medium text-gray-900">
                  {isOverBudget ? 'Over Budget!' : remainingBudget < 10 ? 'Close to Target!' : 'Budget Remaining'}
                </span>
              </div>
              {isOverBudget && (
                <p className="text-red-600 text-sm mt-1">
                  Remove ${(totalPrice - targetPrice).toFixed(2)} to get back on track
                </p>
              )}
            </div>
            
            <div className="text-right">
              <div className={`text-2xl font-bold ${
                isOverBudget ? 'text-red-600' : remainingBudget < 10 ? 'text-yellow-600' : 'text-green-600'
              }`}>
                ${Math.abs(remainingBudget).toFixed(2)}
              </div>
              <div className="text-sm text-gray-500">
                {isOverBudget ? 'over' : 'remaining'}
              </div>
            </div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Progress to Target</span>
            <span className="font-medium">
              {Math.min(100, (totalPrice / targetPrice * 100)).toFixed(1)}%
            </span>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-2">
            <motion.div
              className={`h-2 rounded-full transition-all duration-500 ${
                isOverBudget 
                  ? 'bg-red-500' 
                  : totalPrice > targetPrice * 0.9 
                    ? 'bg-yellow-500'
                    : 'bg-green-500'
              }`}
              initial={{ width: 0 }}
              animate={{ 
                width: `${Math.min(100, (totalPrice / targetPrice * 100))}%` 
              }}
            />
          </div>
        </div>

        {/* Final Total */}
        <div className="bg-gradient-to-r from-elastic-blue/5 to-elastic-teal/5 rounded-xl p-4 border border-elastic-blue/20">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="bg-elastic-blue p-1 rounded">
                <ShoppingCart className="h-4 w-4 text-white" />
              </div>
              <span className="font-semibold text-gray-900">Cart Total</span>
            </div>
            
            <div className="text-right">
              <div className={`text-3xl font-bold ${isOverBudget ? 'text-red-600' : 'text-elastic-blue'}`}>
                ${totalPrice.toFixed(2)}
              </div>
              <div className="text-sm text-gray-500">
                Target: ${targetPrice.toFixed(2)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
