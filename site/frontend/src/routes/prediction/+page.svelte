<script>
	import { onMount } from 'svelte';
	let predictionLog = '';
	let loading = false;
	let error = '';

	async function fetchPrediction() {
		loading = true;
		error = '';
		predictionLog = '';

		try {
			const response = await fetch('http://localhost:8080/predict');
			if (!response.ok) {
				throw new Error(`Error: ${response.status} ${response.statusText}`);
			}
			predictionLog = await response.text();
		} catch (err) {
			error = err.message;
		} finally {
			loading = false;
		}
	}
</script>

<div class="container">
	<button class="button" on:click={fetchPrediction} disabled={loading}>
		{loading ? 'Loading...' : 'Get Prediction'}
	</button>

	{#if error}
		<div class="error">{error}</div>
	{/if}

	{#if predictionLog}
		<div class="log">{predictionLog}</div>
	{/if}
</div>

<style>
	.container {
		padding: 1rem;
	}
	.button {
		padding: 0.5rem 1rem;
		font-size: 1rem;
		cursor: pointer;
		background-color: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
	}
	.button:disabled {
		background-color: #ccc;
		cursor: not-allowed;
	}
	.log {
		margin-top: 1rem;
		padding: 1rem;
		background-color: #f8f9fa;
		border: 1px solid #ddd;
		border-radius: 4px;
		white-space: pre-wrap;
		font-family: monospace;
	}
	.error {
		margin-top: 1rem;
		color: red;
		font-weight: bold;
	}
</style>
