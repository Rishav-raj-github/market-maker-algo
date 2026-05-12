import gym
from gym import spaces
import numpy as np
from stable_baselines3 import PPO

class MarketMakingEnv(gym.Env):
    """
    Custom OpenAI Gym Environment for training a Reinforcement Learning agent 
    to act as a market maker.
    """
    def __init__(self):
        super(MarketMakingEnv, self).__init__()
        
        # Action Space: 
        # 0: Hold, 1: Quote Narrow Spread, 2: Quote Wide Spread, 3: Skew Bid, 4: Skew Ask
        self.action_space = spaces.Discrete(5)
        
        # Observation Space: [Inventory, Mid Price, Volatility, Spread, OFI]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(5,), dtype=np.float32)
        
        self.inventory = 0
        self.mid_price = 100.0

    def step(self, action):
        # Simulate market response to quoted spreads
        reward = 0.0
        done = False
        
        # Simplified reward function: + for earning spread, - for inventory risk
        if action == 1:
            reward = 0.01 - abs(self.inventory) * 0.005
        elif action == 2:
            reward = 0.05 - abs(self.inventory) * 0.01
            
        # Update state
        self.mid_price += np.random.normal(0, 0.1)
        obs = np.array([self.inventory, self.mid_price, 0.02, 0.01, 0.0])
        
        return obs, reward, done, {}

    def reset(self):
        self.inventory = 0
        self.mid_price = 100.0
        return np.array([0.0, 100.0, 0.02, 0.01, 0.0])

def train_rl_agent():
    env = MarketMakingEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    print("Training RL Market Maker Agent...")
    model.learn(total_timesteps=10000)
    model.save("rl_market_maker_v1")
    print("Model saved successfully.")

if __name__ == "__main__":
    train_rl_agent()
