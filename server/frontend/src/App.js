import Register from "./components/Register/Register";
import LoginPanel from "./components/Login/Login";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/login/" element={<LoginPanel />} />
      <Route path="/register/" element={<Register />} />
    </Routes>
  );
}

export default App;
