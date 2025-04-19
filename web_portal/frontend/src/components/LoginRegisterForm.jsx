import React from 'react';
import { registerUser, loginUser } from '../api';

function LoginRegisterForm({ onLoginSuccess }) {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [message, setMessage] = React.useState("");

  const handleRegister = async () => {
    const data = await registerUser(email, password);
    if (data.message === "User registered successfully") {
      setMessage("Registration successful. Please log in now.");
    } else {
      setMessage(data.message || "Registration failed");
    }
  };

  const handleLogin = async () => {
    const data = await loginUser(email, password);
    if (data.message === "Login successful") {
      setMessage("Login successful!");
      // In a real app, you'd store data.token
      onLoginSuccess(email);
    } else {
      setMessage(data.message || "Login failed");
    }
  };

  return (
    <div style={{ marginTop: '20px' }}>
      <h2>Register / Login</h2>
      <div style={{ marginBottom: '10px' }}>
        <label>Email: </label><br />
        <input 
          type="email" 
          value={email} 
          onChange={e => setEmail(e.target.value)} 
          placeholder="Enter email" 
        />
      </div>
      <div style={{ marginBottom: '10px' }}>
        <label>Password: </label><br />
        <input 
          type="password" 
          value={password} 
          onChange={e => setPassword(e.target.value)} 
          placeholder="Enter password" 
        />
      </div>
      <button onClick={handleRegister} style={{ marginRight: '10px' }}>Register</button>
      <button onClick={handleLogin}>Login</button>
      <p>{message}</p>
    </div>
  );
}

export default LoginRegisterForm;
