import logo from './logo.svg';
import QueryBar from './components/query_bar';
import IcicleChart from './components/icicleChart';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
      <QueryBar />
      <IcicleChart />
      </header>
    </div>
  );
}

export default App;
