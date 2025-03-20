<script>
    import { onMount } from 'svelte';
  
    let graphData = null;
    let svgContainer;
    let width = 900;
    let height = 600;
    let transform = { x: 0, y: 0, scale: 1 };
    let isDragging = false;
    let dragStart = { x: 0, y: 0 };
    let viewBox = `0 0 ${width} ${height}`;
  
    // Severity colors
    const severityColors = {
      "low": "#4CAF50",    // Green
      "medium": "#FFC107", // Yellow
      "high": "#FF5722",   // Orange
      "critical": "#F44336" // Red
    };
  
    // Sample data structure for testing
    const sampleData = {
      nodes: [
        {
          id: "root",
          label: "192.168.1.0/24",
          severity: "low",
          children: [
            {
              id: "server1",
              label: "192.168.1.10:80",
              path: "/login",
              severity: "medium",
              children: [
                {
                  id: "endpoint1",
                  label: "192.168.1.10:80",
                  path: "/login/auth",
                  severity: "high",
                  children: []
                },
                {
                  id: "endpoint2",
                  label: "192.168.1.10:80",
                  path: "/login/reset",
                  severity: "low",
                  children: []
                }
              ]
            },
            {
              id: "server2",
              label: "192.168.1.20:22",
              severity: "critical",
              children: []
            },
            {
              id: "server3",
              label: "192.168.1.30:443",
              path: "/api",
              severity: "low",
              children: [
                {
                  id: "endpoint3",
                  label: "192.168.1.30:443",
                  path: "/api/users",
                  severity: "medium",
                  children: []
                },
                {
                  id: "endpoint4",
                  label: "192.168.1.30:443",
                  path: "/api/data",
                  severity: "low",
                  children: []
                }
              ]
            }
          ]
        }
      ]
    };
  
    let treeNodes = [];
    let treeLinks = [];
  
    onMount(async () => {
      try {
        // Try to fetch data from API
        const response = await fetch('/api/graph');
        graphData = await response.json();
      } catch (error) {
        console.log("Using sample data:", error);
        // Use sample data if fetch fails
        graphData = sampleData;
      }
  
      processTreeData();
      centerTree();
    });
  
    function processTreeData() {
      if (!graphData) return;
  
      // Reset arrays
      treeNodes = [];
      treeLinks = [];
  
      const rootNode = graphData.nodes[0];
      const nodeSize = { width: 180, height: 60 };
      const levelHeight = 120;
  
      // First pass: calculate the total width needed and count nodes per level
      let levelCounts = {};
      let maxLevel = 0;
  
      function countNodesPerLevel(node, level = 0) {
        if (!levelCounts[level]) levelCounts[level] = 0;
        levelCounts[level]++;
        maxLevel = Math.max(maxLevel, level);
        
        if (node.children && node.children.length > 0) {
          node.children.forEach(child => countNodesPerLevel(child, level + 1));
        }
      }
      
      countNodesPerLevel(rootNode);
  
      // Calculate horizontal spacing for each level
      let horizontalSpacingPerLevel = {};
      for (let level = 0; level <= maxLevel; level++) {
        horizontalSpacingPerLevel[level] = width / (levelCounts[level] + 1);
      }
  
      // Calculate the total width needed for each level
      let levelWidths = {};
      for (let level = 0; level <= maxLevel; level++) {
        levelWidths[level] = horizontalSpacingPerLevel[level] * (levelCounts[level] + 1);
      }
  
      // Second pass: position nodes
      function positionNodes(node, level = 0, levelIndex = 0) {
        const horizontalSpacing = horizontalSpacingPerLevel[level];
        
        // Calculate x position - center the node within its allocated space
        // For the root node (level 0), always center it
        const x = level === 0 ? 
          width / 2 : 
          horizontalSpacing * (levelIndex + 1);
        
        const y = level * levelHeight + 50;
  
        // Add node to the list
        treeNodes.push({
          id: node.id,
          x,
          y,
          label: node.label,
          path: node.path,
          severity: node.severity,
          width: nodeSize.width,
          height: nodeSize.height
        });
  
        // If node has children, position them
        if (node.children && node.children.length > 0) {
          node.children.forEach((child, index) => {
            // Track the current position in this level
            const childLevelIndex = level === 0 ? 
              index : // First level children are positioned sequentially
              levelCounts[level + 1] > 0 ? 
                (levelIndex * node.children.length) + index : // Position based on parent
                index; // Fallback
  
            // Position the child node
            positionNodes(child, level + 1, childLevelIndex);
  
            // Add link to the list (only one connection per parent-child pair)
            treeLinks.push({
              source: node.id,
              target: child.id
            });
          });
        }
      }
  
      // Position all nodes starting from the root
      positionNodes(rootNode);
    }
  
    function handleMouseDown(event) {
      isDragging = true;
      dragStart = { x: event.clientX, y: event.clientY };
    }
  
    function handleMouseUp() {
      isDragging = false;
    }
  
    function handleMouseMove(event) {
      if (!isDragging) return;
  
      const dx = event.clientX - dragStart.x;
      const dy = event.clientY - dragStart.y;
  
      transform.x += dx / transform.scale;
      transform.y += dy / transform.scale;
  
      dragStart = { x: event.clientX, y: event.clientY };
      updateViewBox();
    }
  
    function updateViewBox() {
      viewBox = `${-transform.x} ${-transform.y} ${width / transform.scale} ${height / transform.scale}`;
    }
  
    function handleWheel(event) {
      event.preventDefault();
  
      const scaleChange = event.deltaY > 0 ? 0.9 : 1.1;
      const newScale = Math.max(0.1, Math.min(3, transform.scale * scaleChange));
  
      // Calculate the mouse position relative to the SVG
      const rect = event.currentTarget.getBoundingClientRect();
      const mouseX = event.clientX - rect.left;
      const mouseY = event.clientY - rect.top;
  
      // Convert mouse position to SVG coordinates
      const svgX = mouseX / transform.scale + (-transform.x);
      const svgY = mouseY / transform.scale + (-transform.y);
  
      // Calculate new translate values to zoom to mouse position
      transform.x = -svgX * (newScale / transform.scale) + (mouseX / newScale);
      transform.y = -svgY * (newScale / transform.scale) + (mouseY / newScale);
      transform.scale = newScale;
  
      updateViewBox();
    }
  
    function zoomIn() {
      transform.scale = Math.min(3, transform.scale * 1.3);
      updateViewBox();
    }
  
    function zoomOut() {
      transform.scale = Math.max(0.1, transform.scale * 0.7);
      updateViewBox();
    }
  
    function resetZoom() {
      centerTree();
    }
  
    function centerTree() {
      if (treeNodes.length === 0) return;
  
      // Calculate the center of the tree
      let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
      
      treeNodes.forEach(node => {
        minX = Math.min(minX, node.x - node.width / 2);
        maxX = Math.max(maxX, node.x + node.width / 2);
        minY = Math.min(minY, node.y - node.height / 2);
        maxY = Math.max(maxY, node.y + node.height / 2);
      });
      
      // Calculate the center point of the tree
      const centerX = (minX + maxX) / 2;
      const centerY = (minY + maxY) / 2;
      
      // Center the tree in the viewport
      transform.x = centerX - width / (2 * transform.scale);
      transform.y = centerY - height / (2 * transform.scale);
      
      // Reset scale to fit the entire tree
      const treeWidth = maxX - minX + 100; // Add padding
      const treeHeight = maxY - minY + 100; // Add padding
      
      const scaleX = width / treeWidth;
      const scaleY = height / treeHeight;
      transform.scale = Math.min(scaleX, scaleY, 1) * 0.9; // 90% of the calculated scale for padding
      
      updateViewBox();
    }
  </script>
  
  <div class="container">
    <aside class="sidebar">
      <div class="logo">
        <h2>TRACE</h2>
      </div>
  
      <nav>
        <ul>
          <li><a href="/dashboard">Dashboard</a></li>
          <li><a href="/scans">Scan Results</a></li>
          <li class="active"><a href="/tree-view">Tree View</a></li>
          <li><a href="/settings">Settings</a></li>
          <li><a href="/reports">Reports</a></li>
        </ul>
      </nav>
  
      <div class="sidebar-footer">
        <span>TRACE System v1.0</span>
      </div>
    </aside>
    
    <div class="main-content">
      <h1>TRACE System Tree View</h1>
      <div class="graph-container" bind:this={svgContainer}>
        <svg
          width="100%"
          height="100%"
          {viewBox}
          style="font: 12px sans-serif;"
          on:mousedown={handleMouseDown}
          on:mouseup={handleMouseUp}
          on:mouseleave={handleMouseUp}
          on:mousemove={handleMouseMove}
          on:wheel={handleWheel}
        >
          <!-- Links -->
          {#each treeLinks as link}
            {@const sourceNode = treeNodes.find(n => n.id === link.source)}
            {@const targetNode = treeNodes.find(n => n.id === link.target)}
            {#if sourceNode && targetNode}
              <line
                x1={sourceNode.x}
                y1={sourceNode.y + sourceNode.height / 2}
                x2={targetNode.x}
                y2={targetNode.y - targetNode.height / 2}
                stroke="#999"
                stroke-width="1.5"
                stroke-opacity="0.7"
              />
            {/if}
          {/each}
  
          <!-- Nodes -->
          {#each treeNodes as node}
            <g transform={`translate(${node.x - node.width / 2}, ${node.y - node.height / 2})`}>
              <!-- Node rectangle -->
              <rect
                width={node.width}
                height={node.height}
                rx="5"
                ry="5"
                fill="white"
                stroke="#333"
                stroke-width="1"
              />
  
              <!-- Severity bar -->
              <rect
                class="severity-bar"
                width={node.width - 20}
                height="8"
                x="10"
                y="5"
                rx="3"
                ry="3"
                fill={severityColors[node.severity] || "#ccc"}
              />
  
              <!-- Node label (IP:port) -->
              <text
                class="node-label"
                x={node.width / 2}
                y="25"
                text-anchor="middle"
                font-weight="bold"
              >
                {node.label || ""}
              </text>
  
              <!-- Path label -->
              <text
                class="path-label"
                x={node.width / 2}
                y="45"
                text-anchor="middle"
                fill="#666"
              >
                {node.path || ""}
              </text>
  
              <!-- Severity label text -->
              <text
                class="severity-text"
                x={node.width / 2}
                y="18"
                text-anchor="middle"
                font-size="9px"
              >
                {node.severity?.toUpperCase() || ""}
              </text>
            </g>
          {/each}
        </svg>
      </div>
  
      <div class="zoom-controls">
        <button on:click={zoomIn} class="zoom-btn">
          <span class="zoom-icon">+</span>
        </button>
        <button on:click={resetZoom} class="zoom-btn">
          <span class="zoom-icon">⟲</span>
        </button>
        <button on:click={zoomOut} class="zoom-btn">
          <span class="zoom-icon">-</span>
        </button>
      </div>
    </div>
  </div>
  
  <style>
    /* Container layout */
    .container {
      display: flex;
      height: 100vh;
      width: 100%;
    }
    
    /* Sidebar styles */
    .sidebar {
      width: 220px;
      background-color: #2c3e50;
      color: white;
      display: flex;
      flex-direction: column;
      height: 100%;
      box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    }
    
    .logo {
      padding: 20px;
      background-color: #1a2632;
      text-align: center;
    }
    
    .logo h2 {
      margin: 0;
      font-size: 24px;
      font-weight: bold;
    }
    
    nav {
      flex-grow: 1;
      padding: 20px 0;
    }
    
    nav ul {
      list-style-type: none;
      padding: 0;
      margin: 0;
    }
    
    nav ul li {
      padding: 10px 20px;
      transition: background-color 0.3s;
    }
    
    nav ul li:hover {
      background-color: #3a526a;
    }
    
    nav ul li a {
      color: #ecf0f1;
      text-decoration: none;
      display: block;
    }
    
    nav ul li.active {
      background-color: #3498db;
    }
    
    .sidebar-footer {
      padding: 15px;
      text-align: center;
      font-size: 12px;
      background-color: #1a2632;
    }
    
    /* Main content styles */
    .main-content {
      flex-grow: 1;
      padding: 20px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    
    h1 {
      margin-top: 0;
      color: #2c3e50;
    }
    
    .graph-container {
      flex-grow: 1;
      overflow: hidden;
      border: 1px solid #e0e0e0;
      border-radius: 5px;
      background-color: #f9f9f9;
    }
    
    /* Zoom controls */
    .zoom-controls {
      display: flex;
      justify-content: center;
      padding: 10px;
      gap: 10px;
    }
    
    .zoom-btn {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background-color: white;
      border: 1px solid #ddd;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .zoom-btn:hover {
      background-color: #f0f0f0;
    }
    
    .zoom-icon {
      font-size: 18px;
      line-height: 1;
    }
  </style>