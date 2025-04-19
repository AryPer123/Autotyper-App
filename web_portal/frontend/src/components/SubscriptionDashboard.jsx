import React from 'react';
import { subscribeUser, verifySubscription } from '../api';

function SubscriptionDashboard({ userEmail }) {
  const [status, setStatus] = React.useState(null);

  React.useEffect(() => {
    handleVerify();
  }, []);

  const handleVerify = async () => {
    const data = await verifySubscription(userEmail);
    if (data.status === "active") {
      setStatus("active");
    } else if (data.status === "expired") {
      setStatus("expired");
    } else {
      setStatus("inactive");
    }
  };

  const handleSubscribe = async () => {
    // For example, subscribe for 30 days
    const data = await subscribeUser(userEmail, 30);
    alert(data.message);
    // Refresh subscription status
    handleVerify();
  };

  return (
    <div>
      <h2>Subscription Dashboard</h2>
      <p>Logged in as: {userEmail}</p>
      <p>Subscription status: {status}</p>
      <button onClick={handleVerify}>Check Subscription</button>
      <button onClick={handleSubscribe}>Subscribe / Extend 30 days</button>
    </div>
  );
}

export default SubscriptionDashboard;
