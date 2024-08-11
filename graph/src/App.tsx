import React from 'react';
import Graph3D from './components/Graph3D';
import TagForm from './components/Form';

const App: React.FC = () => {
  return (
    <div className="App">
      <TagForm />
      <Graph3D />
    </div>
  );
};

export default App;
