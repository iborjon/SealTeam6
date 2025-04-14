<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
  
	let jsonInput = `{
	"url": "http://example.com",
	"depth": "",
	"max_pages": "2",
	"user_agent": "",
	"delay": "",
	"proxy": ""
  }`;
	let response = writable(null);
	let loading = writable(false);
	let error = writable(null);
  
	async function sendToCrawler() {
	  loading.set(true);
	  error.set(null);
	  try {
		const res = await fetch('http://localhost:8000/crawl', {
		  method: 'POST',
		  headers: { 'Content-Type': 'application/json' },
		  body: jsonInput
		});
		const data = await res.json();
		response.set(data);
	  } catch (err) {
		error.set(err.message);
	  } finally {
		loading.set(false);
	  }
	}
  </script>
  
  <h1 class="text-xl font-bold mb-4">SealTeam6 Crawler</h1>
  
  <textarea bind:value={jsonInput} rows="10" class="w-full p-2 border mb-2 font-mono"></textarea>
  <br />
  <button on:click={sendToCrawler} class="bg-blue-500 text-white px-4 py-2 rounded">Run Crawler</button>
  
  {#if $loading}
	<p>Loading...</p>
  {/if}
  
  {#if $error}
	<p class="text-red-500">Error: {$error}</p>
  {/if}
  
  {#if $response}
	<h2 class="mt-4 text-lg font-semibold">Crawler Results:</h2>
	<pre class="bg-gray-100 p-4 mt-2 overflow-auto">{JSON.stringify($response, null, 2)}</pre>
  {/if}
  