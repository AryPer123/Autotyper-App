import React from 'react';
import SubscriptionDashboard from './components/SubscriptionDashboard';
import LoginRegisterForm from './components/LoginRegisterForm';

function App() {
  const [loggedIn, setLoggedIn] = React.useState(false);
  const [userEmail, setUserEmail] = React.useState("");

  const handleLoginSuccess = (email) => {
    setLoggedIn(true);
    setUserEmail(email);
  };

  return (
    <div style={{ fontFamily: 'sans-serif', margin: '20px' }}>
      <h1>Welcome to CopyAutotyper Web Portal</h1>
      {!loggedIn ? (
        <LoginRegisterForm onLoginSuccess={handleLoginSuccess} />
      ) : (
        <SubscriptionDashboard userEmail={userEmail} />
      )}
    </div>
  );
}

export default App;
