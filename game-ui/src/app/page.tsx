'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useGameStore } from '@/store/gameStore';
import { AccessCodeForm } from '@/components/AccessCodeForm';
import { AgentSelectorModal } from '@/components/AgentSelectorModal';
import { GameRulesModal } from '@/components/GameRulesModal';
import { AgentChatInterface } from '@/components/AgentChatInterface';
import { ShoppingCart } from '@/components/ShoppingCart';
import { GameTimer } from '@/components/GameTimer';
import { LeaderboardDisplay } from '@/components/LeaderboardDisplay';
import { Button } from '@/components/ui/Button';
import { Toaster } from 'react-hot-toast';
import { 
  Play, 
  RotateCcw, 
  Trophy, 
  Bot, 
  ShoppingBag, 
  Target,
  Sparkles,
  Users,
  HelpCircle
} from 'lucide-react';
import Confetti from 'react-confetti';
import { useWindowSize } from 'react-use';

export default function GameLayout() {
  const {
    isAuthenticated,
    session,
    selectedAgent,
    gameStarted,
    gameEnded,
    currentItems,
    showAgentSelector,
    showGameRules,
    setSelectedAgent,
    startGame,
    endGame,
    reset,
    showRules,
    hideRules,
    showAgents,
    hideAgents,
  } = useGameStore();

  const [showConfetti, setShowConfetti] = useState(false);
  const [gamePhase, setGamePhase] = useState<'login' | 'setup' | 'playing' | 'complete'>('login');
  const { width, height } = useWindowSize();

  // Update game phase based on state
  useEffect(() => {
    if (!isAuthenticated) {
      setGamePhase('login');
    } else if (!gameStarted && !gameEnded) {
      setGamePhase('setup');
    } else if (gameStarted && !gameEnded) {
      setGamePhase('playing');
    } else if (gameEnded) {
      setGamePhase('complete');
      setShowConfetti(true);
      setTimeout(() => setShowConfetti(false), 5000);
    }
  }, [isAuthenticated, gameStarted, gameEnded]);

  const handleStartGame = () => {
    if (!selectedAgent) {
      showAgents();
      return;
    }
    startGame();
  };

  const handleGameComplete = () => {
    endGame();
    // In real implementation, submit score to leaderboard API
  };

  const totalPrice = currentItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const targetPrice = session?.targetPrice || 100;

  if (gamePhase === 'login') {
    return (
      <div className="min-h-screen bg-gradient-radial from-elastic-blue/20 via-white to-elastic-teal/20 flex items-center justify-center p-4">
        <div className="w-full max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
            {/* Left side - Welcome */}
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              animate={{ opacity: 1, x: 0 }}
              className="text-center lg:text-left"
            >
              <div className="mb-8">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3 }}
                  className="w-24 h-24 bg-gradient-to-r from-vegas-gold to-vegas-red rounded-3xl mx-auto lg:mx-0 mb-6 flex items-center justify-center shadow-2xl"
                >
                  <ShoppingBag className="h-12 w-12 text-white" />
                </motion.div>
                
                <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 mb-4">
                  The Price is{' '}
                  <span className="bg-gradient-to-r from-vegas-gold to-vegas-red bg-clip-text text-transparent">
                    Bot
                  </span>
                </h1>
                
                <p className="text-xl text-gray-600 mb-6 leading-relaxed">
                  Challenge yourself to build the perfect $100 grocery cart using AI-powered shopping agents. 
                  Get as close as possible without going over!
                </p>

                <div className="grid grid-cols-2 gap-4 mb-8">
                  <div className="bg-white rounded-xl p-4 shadow-lg border border-gray-200">
                    <div className="flex items-center space-x-2 mb-2">
                      <Target className="h-5 w-5 text-elastic-blue" />
                      <span className="font-semibold text-gray-900">Goal</span>
                    </div>
                    <p className="text-sm text-gray-600">Reach $100 without going over</p>
                  </div>

                  <div className="bg-white rounded-xl p-4 shadow-lg border border-gray-200">
                    <div className="flex items-center space-x-2 mb-2">
                      <Bot className="h-5 w-5 text-elastic-teal" />
                      <span className="font-semibold text-gray-900">AI Agents</span>
                    </div>
                    <p className="text-sm text-gray-600">5 unique shopping experts</p>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-r from-elastic-blue/10 to-elastic-teal/10 rounded-2xl p-6 border border-elastic-blue/20">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="bg-elastic-blue w-8 h-8 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-bold">E</span>
                  </div>
                  <span className="font-semibold text-gray-900">Powered by Elastic Agent Builder</span>
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">
                  Experience the future of AI-powered applications with Elasticsearch's Agent Builder platform.
                  Each shopping agent uses real-time data and intelligent reasoning to help you win.
                </p>
              </div>
            </motion.div>

            {/* Right side - Login Form */}
            <motion.div
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
            >
              <AccessCodeForm onSuccess={() => setGamePhase('setup')} />
            </motion.div>
          </div>
        </div>
        <Toaster position="top-center" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {showConfetti && (
        <Confetti
          width={width}
          height={height}
          recycle={false}
          numberOfPieces={500}
          gravity={0.3}
        />
      )}

      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-vegas-gold to-vegas-red rounded-xl flex items-center justify-center">
                <ShoppingBag className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">The Price is Bot</h1>
                {session && (
                  <p className="text-sm text-gray-600">Welcome, {session.playerName}!</p>
                )}
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center space-x-3">
              <Button
                variant="ghost"
                size="sm"
                onClick={showRules}
                leftIcon={<HelpCircle className="h-4 w-4" />}
              >
                Rules
              </Button>

              {gamePhase === 'setup' && (
                <Button
                  variant="elastic"
                  size="sm"
                  onClick={showAgents}
                  leftIcon={<Bot className="h-4 w-4" />}
                >
                  {selectedAgent ? 'Change Agent' : 'Select Agent'}
                </Button>
              )}

              <Button
                variant="ghost"
                size="sm"
                onClick={reset}
                leftIcon={<RotateCcw className="h-4 w-4" />}
              >
                Reset
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <AnimatePresence mode="wait">
          {/* Setup Phase */}
          {gamePhase === 'setup' && (
            <motion.div
              key="setup"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-8"
            >
              {/* Welcome Banner */}
              <div className="bg-gradient-to-r from-vegas-gold via-vegas-red to-purple-600 rounded-2xl p-6 text-white">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-2xl font-bold mb-2">Ready to Start Shopping?</h2>
                    <p className="text-white/90">
                      Choose your AI agent and begin building your perfect $100 cart!
                    </p>
                  </div>
                  <div className="bg-white/20 p-4 rounded-xl">
                    <Target className="h-8 w-8" />
                  </div>
                </div>
              </div>

              {/* Agent Selection */}
              <div className="bg-white rounded-2xl shadow-lg border border-gray-200 p-6">
                <div className="text-center mb-6">
                  {selectedAgent ? (
                    <div className="flex items-center justify-center space-x-4 mb-4">
                      <div className={`w-16 h-16 ${selectedAgent.color} rounded-2xl flex items-center justify-center`}>
                        <span className="text-white text-2xl">{selectedAgent.avatar}</span>
                      </div>
                      <div className="text-left">
                        <h3 className="text-xl font-bold text-gray-900">{selectedAgent.name}</h3>
                        <p className="text-gray-600">{selectedAgent.description}</p>
                      </div>
                    </div>
                  ) : (
                    <div className="mb-4">
                      <div className="w-16 h-16 bg-gray-200 rounded-2xl flex items-center justify-center mx-auto mb-4">
                        <Bot className="h-8 w-8 text-gray-400" />
                      </div>
                      <h3 className="text-xl font-bold text-gray-900 mb-2">Choose Your Agent</h3>
                      <p className="text-gray-600">Select an AI shopping expert to help you win!</p>
                    </div>
                  )}

                  <div className="flex justify-center space-x-4">
                    <Button
                      variant="elastic"
                      onClick={showAgents}
                      leftIcon={<Bot className="h-5 w-5" />}
                    >
                      {selectedAgent ? 'Change Agent' : 'Select Agent'}
                    </Button>

                    {selectedAgent && (
                      <Button
                        variant="vegas"
                        onClick={handleStartGame}
                        leftIcon={<Play className="h-5 w-5" />}
                      >
                        Start Game
                      </Button>
                    )}
                  </div>
                </div>
              </div>

              {/* Preview Leaderboard */}
              <LeaderboardDisplay limit={5} />
            </motion.div>
          )}

          {/* Playing Phase */}
          {gamePhase === 'playing' && (
            <motion.div
              key="playing"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="grid grid-cols-1 lg:grid-cols-3 gap-6"
            >
              {/* Left Column - Chat */}
              <div className="lg:col-span-2 space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {selectedAgent && (
                      <div className={`w-10 h-10 ${selectedAgent.color} rounded-xl flex items-center justify-center`}>
                        <span className="text-white text-lg">{selectedAgent.avatar}</span>
                      </div>
                    )}
                    <div>
                      <h2 className="text-xl font-bold text-gray-900">
                        Shopping with {selectedAgent?.name}
                      </h2>
                      <p className="text-gray-600">Tell your agent what you're looking for!</p>
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <div className="text-2xl font-bold text-elastic-blue">
                      ${totalPrice.toFixed(2)}
                    </div>
                    <div className="text-sm text-gray-500">of ${targetPrice}</div>
                  </div>
                </div>

                <AgentChatInterface className="h-96" />
              </div>

              {/* Right Column - Cart & Timer */}
              <div className="space-y-6">
                <GameTimer
                  onTimeUp={handleGameComplete}
                  className="sticky top-24"
                />
                
                <ShoppingCart className="sticky top-44" />

                {currentItems.length > 0 && (
                  <div className="text-center">
                    <Button
                      variant="vegas"
                      size="lg"
                      onClick={handleGameComplete}
                      className="w-full"
                    >
                      Complete Game & Submit Score
                    </Button>
                  </div>
                )}
              </div>
            </motion.div>
          )}

          {/* Complete Phase */}
          {gamePhase === 'complete' && (
            <motion.div
              key="complete"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="space-y-8"
            >
              {/* Results Banner */}
              <div className="bg-gradient-to-r from-vegas-gold via-vegas-red to-purple-600 rounded-2xl p-8 text-white text-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ delay: 0.3 }}
                  className="mb-6"
                >
                  <div className="w-20 h-20 bg-white/20 rounded-3xl mx-auto mb-4 flex items-center justify-center">
                    <Trophy className="h-10 w-10" />
                  </div>
                  <h2 className="text-3xl font-bold mb-2">Game Complete! 🎉</h2>
                  <p className="text-white/90 text-lg">
                    You built a ${totalPrice.toFixed(2)} cart with {selectedAgent?.name}!
                  </p>
                </motion.div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm">
                    <div className="text-2xl font-bold">${totalPrice.toFixed(2)}</div>
                    <div className="text-white/80 text-sm">Final Total</div>
                  </div>
                  <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm">
                    <div className="text-2xl font-bold">{currentItems.length}</div>
                    <div className="text-white/80 text-sm">Items</div>
                  </div>
                  <div className="bg-white/10 rounded-xl p-4 backdrop-blur-sm">
                    <div className="text-2xl font-bold">95.2</div>
                    <div className="text-white/80 text-sm">Score</div>
                  </div>
                </div>

                <div className="flex justify-center space-x-4">
                  <Button
                    variant="secondary"
                    onClick={reset}
                    leftIcon={<RotateCcw className="h-5 w-5" />}
                  >
                    Play Again
                  </Button>
                  <Button
                    variant="ghost"
                    leftIcon={<Users className="h-5 w-5" />}
                  >
                    View Leaderboard
                  </Button>
                </div>
              </div>

              {/* Final Cart */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <ShoppingCart />
                <LeaderboardDisplay />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>

      {/* Modals */}
      <AgentSelectorModal
        isOpen={showAgentSelector}
        onClose={hideAgents}
        onSelectAgent={setSelectedAgent}
      />

      <GameRulesModal
        isOpen={showGameRules}
        onClose={hideRules}
      />

      <Toaster position="top-center" />
    </div>
  );
}
