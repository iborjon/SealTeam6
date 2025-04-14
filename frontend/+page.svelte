<script>
  import { onMount } from 'svelte';
  import "../styles/styles.css";  // Import our custom CSS file

  // API base URL (adjust as needed)
  const API_BASE_URL = "http://localhost:5173";

  // Hardcoded list of lead analyst initials
  const LEAD_ANALYST_INITIALS = ['ADP', 'CR', 'BG', 'SQ', 'DR', 'TH', 'LRM', 'MO'];

  // State variables
  let isLoggedIn = false;
  let userName = "";
  let userInitials = "";
  let isLeadAnalyst = false;
  let errorMessage = "";
  // Which view to show: "login", "dashboard", "createProject", "projectList", "folders", "joinProject"
  let currentView = "login";

  // Data fetched from the API
  let dashboardData = { my_projects: [], shared_projects: [] };
  let folders = [];
  let foldersError = "";

  // Fields for creating a new project
  let projectName = "";
  let description = "";
  let machine_IP = "";
  let status = "";
  let leadAnalystInitials = "";
  let locked = "false";
  let projectFiles = [];

  // --- Authentication Functions ---
  async function handleLogin(e) {
    e.preventDefault();
    if (!userName.trim() || !userInitials.trim()) {
      errorMessage = "Please enter both your name and initials";
      return;
    }
    // Determine lead analyst role
    isLeadAnalyst = LEAD_ANALYST_INITIALS.includes(userInitials.toUpperCase());
    isLoggedIn = true;
    errorMessage = "";
    currentView = "dashboard";
    loadDashboard();
  }

  function handleLogout() {
    isLoggedIn = false;
    userName = "";
    userInitials = "";
    isLeadAnalyst = false;
    currentView = "login";
  }

  function navigateTo(view) {
    currentView = view;
    if (view === "dashboard") {
      loadDashboard();
    } else if (view === "folders") {
      loadFolders();
    }
  }

  // --- Load Dashboard Data ---
  async function loadDashboard() {
    try {
      const res = await fetch(`${API_BASE_URL}/`);
      if (!res.ok) throw new Error("Failed to load dashboard data");
      dashboardData = await res.json();
    } catch (err) {
      console.error(err);
      errorMessage = err.message;
    }
  }

  // --- Create Project ---
  async function handleCreateProject(e) {
    e.preventDefault();
    const formData = new FormData();
    formData.append("project_name", projectName);
    formData.append("description", description);
    formData.append("machine_IP", machine_IP);
    formData.append("status", status);
    // Use either a dedicated lead analyst input or default to the logged-in user's initials
    formData.append("lead_analyst_initials", leadAnalystInitials || userInitials);
    formData.append("locked", locked);
    projectFiles.forEach(file => {
      formData.append("files", file);
    });
    try {
      const res = await fetch(`${API_BASE_URL}/create/`, {
        method: "POST",
        body: formData
      });
      if (!res.ok) throw new Error("Failed to create project");
      const result = await res.json();
      if (result.status === "success") {
        alert("Project created successfully");
        // Reset fields if necessary
        projectName = "";
        description = "";
        machine_IP = "";
        status = "";
        leadAnalystInitials = "";
        locked = "false";
        projectFiles = [];
        navigateTo("dashboard");
      }
    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  }

  // --- Operations: Delete, Restore, Lock, Unlock ---
  async function deleteProject(projectNameToDelete) {
    try {
      const res = await fetch(`${API_BASE_URL}/delete/${encodeURIComponent(projectNameToDelete)}`, {
        method: "POST"
      });
      const result = await res.json();
      if (result.status === "success") {
        alert(`Project "${projectNameToDelete}" deleted`);
        loadDashboard();
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function restoreProject(projectNameToRestore) {
    try {
      const res = await fetch(`${API_BASE_URL}/restore/${encodeURIComponent(projectNameToRestore)}`, {
        method: "POST"
      });
      const result = await res.json();
      if (result.status === "success") {
        alert(`Project "${projectNameToRestore}" restored`);
        loadDashboard();
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function lockProject(projectNameToLock) {
    try {
      const res = await fetch(`${API_BASE_URL}/lock/${encodeURIComponent(projectNameToLock)}/${userInitials}`, {
        method: "POST"
      });
      const result = await res.json();
      if (result.status === "success") {
        alert(`Project "${projectNameToLock}" locked`);
        loadDashboard();
      }
    } catch (err) {
      console.error(err);
    }
  }

  async function unlockProject(projectNameToUnlock) {
    try {
      const res = await fetch(`${API_BASE_URL}/unlock/${encodeURIComponent(projectNameToUnlock)}/${userInitials}`, {
        method: "POST"
      });
      const result = await res.json();
      if (result.status === "success") {
        alert(`Project "${projectNameToUnlock}" unlocked`);
        loadDashboard();
      }
    } catch (err) {
      console.error(err);
    }
  }

  // --- Load Folders ---
  async function loadFolders() {
    try {
      const res = await fetch(`${API_BASE_URL}/folders/`);
      if (!res.ok) throw new Error("Failed to load folders");
      const data = await res.json();
      folders = data.my_folders;
    } catch (err) {
      foldersError = err.message;
      console.error(err);
    }
  }
</script>


{#if !isLoggedIn}
  <!-- LOGIN VIEW -->
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <form on:submit={handleLogin} class="bg-white p-6 rounded shadow-md">
      <h2 class="text-xl font-bold mb-4">Welcome to TRACE</h2>
      {#if errorMessage}
        <p class="error mb-4">{errorMessage}</p>
      {/if}
      <div class="mb-4">
        <label class="block mb-1">Full Name</label>
        <input type="text" bind:value={userName} class="border p-2 w-full" />
      </div>
      <div class="mb-4">
        <label class="block mb-1">Initials</label>
        <input type="text" bind:value={userInitials} class="border p-2 w-full" />
      </div>
      <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Start</button>
    </form>
  </div>
{:else}
  <!-- LOGGED IN VIEW -->
  <header class="bg-white shadow p-4 flex justify-between items-center">
    <h1 class="text-2xl font-bold">TRACE</h1>
    <div>
      <span>Signed in as: <strong>{userName}</strong> {isLeadAnalyst ? "(Lead Analyst)" : ""}</span>
      <button on:click={handleLogout} class="ml-4 bg-gray-200 px-3 py-1 rounded">Logout</button>
    </div>
  </header>
  <nav class="bg-blue-50 p-4 flex space-x-4">
    <button on:click={() => navigateTo("dashboard")} class="px-3 py-1 bg-blue-300 rounded">Dashboard</button>
    {#if isLeadAnalyst}
      <button on:click={() => navigateTo("createProject")} class="px-3 py-1 bg-green-300 rounded">Create Project</button>
    {/if}
    <button on:click={() => navigateTo("projectList")} class="px-3 py-1 bg-yellow-300 rounded">Project List</button>
    <button on:click={() => navigateTo("folders")} class="px-3 py-1 bg-purple-300 rounded">Folders</button>
    <button on:click={() => navigateTo("joinProject")} class="px-3 py-1 bg-indigo-300 rounded">Join Project</button>
  </nav>
  <main class="p-4">
    {#if currentView === "dashboard"}
      <h2 class="text-xl font-bold mb-4">Dashboard</h2>
      <section class="mb-6">
        <h3 class="text-lg font-semibold">My Projects</h3>
        <ul>
          {#each dashboardData.my_projects as project}
            <li class="border p-2 mb-2">
              <strong>{project.name}</strong> – Last Edited: {project.last_edit_date}
              <!-- Example action buttons -->
              <button on:click={() => deleteProject(project.name)} class="ml-2 bg-red-300 px-2 py-1 rounded">Delete</button>
              {#if isLeadAnalyst}
                <button on:click={() => lockProject(project.name)} class="ml-2 bg-yellow-300 px-2 py-1 rounded">Lock</button>
                <button on:click={() => unlockProject(project.name)} class="ml-2 bg-green-300 px-2 py-1 rounded">Unlock</button>
              {/if}
            </li>
          {/each}
        </ul>
      </section>
      <section>
        <h3 class="text-lg font-semibold">Shared Projects</h3>
        <ul>
          {#each dashboardData.shared_projects as project}
            <li class="border p-2 mb-2">
              <strong>{project.name}</strong> – Last Edited: {project.last_edit_date}
              <button on:click={() => alert("Join project " + project.name)} class="ml-2 bg-purple-300 px-2 py-1 rounded">Join</button>
            </li>
          {/each}
        </ul>
      </section>
    {:else if currentView === "createProject" && isLeadAnalyst}
      <h2 class="text-xl font-bold mb-4">Create New Project</h2>
      <form on:submit={handleCreateProject} class="bg-white p-6 rounded shadow max-w-lg mx-auto">
        <div class="mb-4">
          <label class="block mb-1">Project Name</label>
          <input type="text" bind:value={projectName} class="border p-2 w-full" required />
        </div>
        <div class="mb-4">
          <label class="block mb-1">Description</label>
          <input type="text" bind:value={description} class="border p-2 w-full" required />
        </div>
        <div class="mb-4">
          <label class="block mb-1">Machine IP</label>
          <input type="text" bind:value={machine_IP} class="border p-2 w-full" required />
        </div>
        <div class="mb-4">
          <label class="block mb-1">Status</label>
          <input type="text" bind:value={status} class="border p-2 w-full" required />
        </div>
        <div class="mb-4">
          <label class="block mb-1">Locked</label>
          <select bind:value={locked} class="border p-2 w-full">
            <option value="true">Yes</option>
            <option value="false">No</option>
          </select>
        </div>
        <!-- Optionally, add an input for Lead Analyst Initials if required -->
        <div class="mb-4">
          <label class="block mb-1">Lead Analyst Initials</label>
          <input type="text" bind:value={leadAnalystInitials} class="border p-2 w-full" placeholder="Optional; defaults to your initials" />
        </div>
        <div class="mb-4">
          <label class="block mb-1">Upload Files (optional)</label>
          <input type="file" multiple on:change={(e) => { projectFiles = [...e.target.files]; }} class="border p-2 w-full" />
        </div>
        <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">Create Project</button>
      </form>
    {:else if currentView === "projectList"}
      <h2 class="text-xl font-bold mb-4">Project List</h2>
      <ul>
        {#each dashboardData.my_projects as project}
          <li class="border p-2 mb-2">
            <strong>{project.name}</strong> – Last Edited: {project.last_edit_date}
            <button on:click={() => alert("Open project " + project.name)} class="ml-2 bg-blue-300 px-2 py-1 rounded">Open</button>
          </li>
        {/each}
      </ul>
    {:else if currentView === "folders"}
      <h2 class="text-xl font-bold mb-4">Project Folders</h2>
      {#if foldersError}
        <p class="error">{foldersError}</p>
      {:else}
        <ul>
          {#each folders as folder}
            <li class="border p-2 mb-2">{folder.path}</li>
          {/each}
        </ul>
      {/if}
    {:else if currentView === "joinProject"}
      <h2 class="text-xl font-bold mb-4">Join a Project</h2>
      <ul>
        {#each dashboardData.shared_projects as project}
          <li class="border p-2 mb-2">
            <strong>{project.name}</strong> – Last Edited: {project.last_edit_date}
            <button on:click={() => alert("Join project " + project.name)} class="ml-2 bg-indigo-300 px-2 py-1 rounded">Join</button>
          </li>
        {/each}
      </ul>
    {/if}
  </main>
{/if}
