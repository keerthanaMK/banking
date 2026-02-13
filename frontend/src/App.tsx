import React from 'react';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>FD Management System</h1>
        <p>Welcome to the Fixed Deposit Management System</p>
      </header>
      <main>
        <section>
          <h2>Create Fixed Deposit</h2>
          <form>
            <label htmlFor="amount">Deposit Amount:</label>
            <input type="number" id="amount" required />

            <label htmlFor="duration">Duration (in years):</label>
            <input type="number" id="duration" required />

            <button type="submit">Create FD</button>
          </form>
        </section>
        <section>
          <h2>Manage Fixed Deposits</h2>
          {/* Table to display existing FDs will go here */}
        </section>
      </main>
      <footer>
        <p>FD Management System © 2026</p>
      </footer>
    </div>
  );
};

export default App;