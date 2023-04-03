import './App.css';
import React from 'react';
import CheckersGame from './components/CheckersGame';

function App() {
  return (
    <div className="App">
      <header className='App-header'>
        <CheckersGame />
      </header>
    </div>
  );
}

export default App;
