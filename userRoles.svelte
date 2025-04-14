
<script>
  import { onMount } from 'svelte';
  
  // Define hardcoded lead analyst initials for role-based access control
  const LEAD_ANALYST_INITIALS = ['ADP', 'CR', 'BG', 'SQ', 'DR', 'TH', 'LRM', 'MO'];
  
  // State for login, user info, and current view
  let isLoggedIn = false;
  let userInitials = '';
  let userName = '';
  let isLeadAnalyst = false;
  let errorMessage = '';
  let currentView = 'dashboard'; // 'dashboard', 'createProject', etc.
  
  // For project creation form
  let projectName = '';
  let startDate = '';
  let endDate = '';
  
  // Handle login submission
  function handleLogin(e) {
    e.preventDefault();
    
    if (!userName.trim() || !userInitials.trim()) {
      errorMessage = 'Please enter both your name and initials';
      return;
    }
    
    // Check if user is a lead analyst based on hardcoded initials
    isLeadAnalyst = LEAD_ANALYST_INITIALS.includes(userInitials.toUpperCase());
    isLoggedIn = true;
    errorMessage = '';
  }
  
  // Handle logout
  function handleLogout() {
    isLoggedIn = false;
    userInitials = '';
    userName = '';
    isLeadAnalyst = false;
    currentView = 'dashboard';
  }
  
  // Function to navigate between views
  function navigateTo(view) {
    currentView = view;
  }
  
  // Handle project creation
  function handleCreateProject(e) {
    e.preventDefault();
    //this would create the project in the backend
    alert(`Project "${projectName}" created successfully!`);
    navigateTo('dashboard');
  }
  
  // Mock data for projects
  const projects = [
    { id: 1, name: "Base Perimeter Network", createdAt: "2025-02-15", leadAnalyst: "ADP" },
    { id: 2, name: "Internal Network Assessment", createdAt: "2025-03-01", leadAnalyst: "SQ" },
    { id: 3, name: "Web Application Testing", createdAt: "2025-03-10", leadAnalyst: "USER" }
  ];
  
  // Mock data for shared projects
  const sharedProjects = [
    { id: 101, name: "External Service Assessment", createdAt: "2025-02-20", leadAnalyst: "TH", port: 8080 },
    { id: 102, name: "Cloud Infrastructure Review", createdAt: "2025-03-05", leadAnalyst: "LRM", port: 8081 },
    { id: 103, name: "Mobile App Security Testing", createdAt: "2025-03-12", leadAnalyst: "MO", port: 8082 }
  ];
  
  // Update the third project to use the current user's initials
  onMount(() => {
    if (userInitials) {
      projects[2].leadAnalyst = userInitials;
    }
  });
</script>

<div class="min-h-screen bg-gray-50">
  {#if !isLoggedIn}
    <!-- Login Form -->
    <div class="flex items-center justify-center min-h-screen bg-gray-100">
      <div class="w-full max-w-md p-8 space-y-8 bg-white rounded-lg shadow-md">
        <div class="text-center">
          <h1 class="text-3xl font-bold text-gray-900">TRACE</h1>
          <p class="mt-2 text-gray-600">Targeted Reconnaissance for Advanced Content Exploitation</p>
        </div>
        
        <form class="mt-8 space-y-6" on:submit={handleLogin}>
          {#if errorMessage}
            <div class="p-3 text-sm text-red-600 bg-red-100 rounded-md">
              {errorMessage}
            </div>
          {/if}
          
          <div>
            <label for="name" class="block text-sm font-medium text-gray-700">
              Full Name
            </label>
            <input
              id="name"
              name="name"
              type="text"
              required
              bind:value={userName}
              class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter your full name"
            />
          </div>
          
          <div>
            <label for="initials" class="block text-sm font-medium text-gray-700">
              Analyst Initials
            </label>
            <input
              id="initials"
              name="initials"
              type="text"
              required
              bind:value={userInitials}
              class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter your initials (e.g., ABC)"
            />
          </div>
          
          <div>
            <button
              type="submit"
              class="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Sign in
            </button>
          </div>
        </form>
      </div>
    </div>
  {:else}
    <!-- Header when logged in -->
    <header class="bg-white shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-2xl font-bold text-blue-600">TRACE</h1>
            </div>
          </div>
          <div class="flex items-center">
            <div class="flex items-center">
              <span class="text-sm font-medium text-gray-500 mr-4">
                Signed in as: <span class="font-bold text-gray-700">{userName}</span>
                {#if isLeadAnalyst}
                  <span class="ml-1 text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">Lead Analyst</span>
                {/if}
              </span>
              <button
                on:click={handleLogout}
                class="px-3 py-1 text-sm text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                Sign out
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
    
    <!-- Main content based on current view -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      {#if currentView === 'dashboard'}
        <!-- Dashboard -->
        <div class="p-6">
          <h2 class="text-2xl font-bold mb-6">Project Dashboard</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div class="p-6 bg-white rounded-lg shadow-md">
              <h3 class="text-lg font-semibold mb-2">Recent Projects</h3>
              <p class="text-gray-600 mb-4">Access your recently opened projects</p>
              <button 
                on:click={() => navigateTo('projectList')}
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                View Projects
              </button>
            </div>
            
            {#if isLeadAnalyst}
              <div class="p-6 bg-white rounded-lg shadow-md">
                <h3 class="text-lg font-semibold mb-2">Create New Project</h3>
                <p class="text-gray-600 mb-4">Start a new penetration testing project</p>
                <button 
                  on:click={() => navigateTo('createProject')}
                  class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                >
                  Create Project
                </button>
              </div>
            {/if}
            
            <div class="p-6 bg-white rounded-lg shadow-md">
              <h3 class="text-lg font-semibold mb-2">Join Project</h3>
              <p class="text-gray-600 mb-4">Join an existing project</p>
              <button 
                on:click={() => navigateTo('joinProject')}
                class="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700"
              >
                Join Project
              </button>
            </div>
          </div>
        </div>
      {:else if currentView === 'createProject' && isLeadAnalyst}
        <!-- Project Creation Form -->
        <div class="p-6">
          <div class="flex items-center mb-6">
            <button 
              on:click={() => navigateTo('dashboard')}
              class="mr-4 text-blue-600 hover:text-blue-800"
            >
              ← Back to Dashboard
            </button>
            <h2 class="text-2xl font-bold">Create New Project</h2>
          </div>
          
          <div class="max-w-2xl bg-white rounded-lg shadow-md p-6">
            <form on:submit={handleCreateProject} class="space-y-6">
              <div>
                <label for="projectName" class="block text-sm font-medium text-gray-700">
                  Project Name
                </label>
                <input
                  id="projectName"
                  name="projectName"
                  type="text"
                  required
                  bind:value={projectName}
                  class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Enter project name"
                />
              </div>
              
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label for="startDate" class="block text-sm font-medium text-gray-700">
                    Start Date
                  </label>
                  <input
                    id="startDate"
                    name="startDate"
                    type="date"
                    required
                    bind:value={startDate}
                    class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
                
                <div>
                  <label for="endDate" class="block text-sm font-medium text-gray-700">
                    End Date
                  </label>
                  <input
                    id="endDate"
                    name="endDate"
                    type="date"
                    required
                    bind:value={endDate}
                    class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </div>
              
              <div>
                <label for="leadAnalyst" class="block text-sm font-medium text-gray-700">
                  Lead Analyst
                </label>
                <input
                  id="leadAnalyst"
                  name="leadAnalyst"
                  type="text"
                  disabled
                  value={`${userName} (${userInitials})`}
                  class="w-full px-3 py-2 mt-1 border border-gray-300 rounded-md shadow-sm bg-gray-50"
                />
              </div>
              
              <div class="flex items-center justify-end space-x-3">
                <button
                  type="button"
                  on:click={() => navigateTo('dashboard')}
                  class="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  class="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                  Create Project
                </button>
              </div>
            </form>
          </div>
        </div>
      {:else if currentView === 'projectList'}
        <!-- Project List -->
        <div class="p-6">
          <div class="flex items-center mb-6">
            <button 
              on:click={() => navigateTo('dashboard')}
              class="mr-4 text-blue-600 hover:text-blue-800"
            >
              ← Back to Dashboard
            </button>
            <h2 class="text-2xl font-bold">Project List</h2>
          </div>
          
          <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Project Name
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created Date
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Lead Analyst
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                {#each projects as project (project.id)}
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900">{project.name}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-500">{project.createdAt}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-500">{project.leadAnalyst}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <button class="text-blue-600 hover:text-blue-800 mr-3">
                        Open
                      </button>
                      {#if isLeadAnalyst && project.leadAnalyst === userInitials}
                        <button class="text-red-600 hover:text-red-800 mr-3">
                          Delete
                        </button>
                        <button class="text-yellow-600 hover:text-yellow-800">
                          Lock
                        </button>
                      {/if}
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      {:else if currentView === 'joinProject'}
        <!-- Join Project -->
        <div class="p-6">
          <div class="flex items-center mb-6">
            <button 
              on:click={() => navigateTo('dashboard')}
              class="mr-4 text-blue-600 hover:text-blue-800"
            >
              ← Back to Dashboard
            </button>
            <h2 class="text-2xl font-bold">Join Project</h2>
          </div>
          
          <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Project Name
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Created Date
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Lead Analyst
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Port
                  </th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Action
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                {#each sharedProjects as project (project.id)}
                  <tr>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-900">{project.name}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-500">{project.createdAt}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-500">{project.leadAnalyst}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <div class="text-sm text-gray-500">{project.port}</div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <button 
                        class="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                        on:click={() => alert(`Joined project: ${project.name}`)}
                      >
                        Join
                      </button>
                    </td>
                  </tr>
                {/each}
              </tbody>
            </table>
          </div>
        </div>
      {/if}
    </main>
  {/if}
</div>


