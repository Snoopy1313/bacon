import { useState } from 'react'
import './App.css'

function App() {
  const [source, setSource] = useState("");
  const [target, setTarget] = useState("");
  const [distance, setDistance] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    let response = await fetch(`http://localhost:5000/get_bacon_distance/${source}/${target}`);
    if (response.status == 400) {
      setDistance("No such Actor")
    }
    else if (response.status == 200) {
      let myText = await response.text();
      setDistance(myText)
    }
    else {
      setDistance("Some error occurred")
    }
  };

  return (
      <form onSubmit={handleSubmit}>
          <label>Actors ID</label>
          <input
            type="text"
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="Type something..."
          />
          <input
            type="text"
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="Type something..."
          />
        <button type="submit">
          Submit
        </button>
        <label>Bacon distance: {distance}</label>
      </form>
    )
}

export default App
