<script>
  import "../styles/styles.css";  // Import our custom CSS file

  // Set the API base URL to the FastAPI backend (adjust as needed)
  const API_BASE_URL = "http://localhost:8000";

  // State variables for the login form
  let userName = "";
  let userInitials = "";
  let errorMessage = "";

  async function handleLogin(e) {
    e.preventDefault();
    
    if (!userName.trim() || !userInitials.trim()) {
      errorMessage = "Please enter both your name and initials";
      return;
    }
    
    // Call the backend to check if the initials are valid
    try {
      const response = await fetch(`${API_BASE_URL}/check_initials?initials=${userInitials}`);
      if (!response.ok) {
        throw new Error("Failed to verify initials");
      }
      const data = await response.json();
      if (data.is_valid) {
        // If valid, redirect to the other team’s dashboard
        window.location.href = API_BASE_URL + "/";
      } else {
        errorMessage = "Invalid initials. You do not have permission to access the dashboard.";
      }
    } catch (err) {
      console.error(err);
      errorMessage = "Error connecting to the verification service.";
    }
  }
</script>

<style>
  /* Increase the welcome box size as a fixed square */
  .welcome-box {
    width: 500px;
    height: 500px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 2rem;
    box-sizing: border-box;
  }
  /* Increase font sizes for uniform appearance */
  .welcome-box h2 {
    font-size: 2.5rem;  /* Larger header text */
    margin-bottom: 1rem;
    text-align: center;
  }
  .welcome-box label {
    font-size: 1.25rem;
    margin-bottom: 0.5rem;
    display: block;
  }
  .welcome-box input {
    font-size: 1.25rem;
    padding: 0.75rem;
    width: 100%;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .welcome-box button {
    font-size: 1.25rem;
    padding: 0.75rem;
    width: 100%;
    background-color: #3b82f6; /* blue-500 */
    color: white;
    border: none;
    border-radius: 4px;
  }
  .error {
    color: red;
    font-size: 1.25rem;
  }
</style>

<!-- Welcome/Login Page -->
<div class="min-h-screen flex items-center justify-center bg-gray-100">
  <form on:submit={handleLogin} class="welcome-box bg-white rounded shadow-md">
    <h2>Welcome to TRACE</h2>
    {#if errorMessage}
      <p class="error">{errorMessage}</p>
    {/if}
    <div class="mb-4">
      <label>Full Name</label>
      <input type="text" bind:value={userName} />
    </div>
    <div class="mb-4">
      <label>Initials</label>
      <input type="text" bind:value={userInitials} />
    </div>
    <button type="submit">Start</button>
  </form>
</div>
