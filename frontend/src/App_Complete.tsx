import React, { useState } from 'react';

// AI Agent for Fixed Deposit (FD) Creation
const AIAgent: React.FC = () => {
  const [amount, setAmount] = useState<number>(0);
  const [duration, setDuration] = useState<number>(0);
  const [interestRate, setInterestRate] = useState<number>(0);
  const [fdDetails, setFdDetails] = useState<string>('');

  const handleFDCreation = () => {
    // Simple AI logic to calculate FD details
    setInterestRate(5); // Assuming a static interest rate for simplification
    const totalAmount = amount + (amount * interestRate * duration) / 100;
    setFdDetails(`Total amount after ${duration} years: $${totalAmount}`);
  };

  return (
    <div>
      <h1>Create Fixed Deposit</h1>
      <input 
        type='number' 
        placeholder='Amount' 
        value={amount} 
        onChange={e => setAmount(Number(e.target.value))} 
      />
      <input 
        type='number' 
        placeholder='Duration (Years)' 
        value={duration} 
        onChange={e => setDuration(Number(e.target.value))} 
      />
      <button onClick={handleFDCreation}>Create FD</button>
      <p>{fdDetails}</p>
    </div>
  );
};

// Main App Component
const App: React.FC = () => {
  return (
    <div>
      <AIAgent />
    </div>
  );
};

export default App;