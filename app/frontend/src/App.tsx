import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/NavBar';
import MapDisplay from './components/MapDisplay';
import Login from './components/Login';
import Register from './components/Register';
import ProtectedRoute from './components/ProtectedRoute';
import { AuthProvider } from './context/AuthContext';

const App = () => {
  return (
    <AuthProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<MapDisplay />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Protected routes will go here */}
          <Route element={<ProtectedRoute />}>
            {/* Add protected pages here later */}
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
