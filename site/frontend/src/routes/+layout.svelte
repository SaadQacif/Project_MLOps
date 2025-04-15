<script lang="ts">
	import '../app.css';
	let { children } = $props();
</script>

{#snippet nav_el(element: { name: String; url: String })}
	<li
		class="grid justify-center border-red-900 transition duration-300 ease-in-out hover:-translate-y-1 hover:scale-110 hover:rounded-md hover:border hover:border-red-800 hover:drop-shadow-lg"
	>
		<a class="grid content-center pl-10 pl-4 pr-10 pr-4 font-mono text-red-50" href="/{element.url}"
			>{element.name}</a
		>
	</li>
{/snippet}
<div class="grid justify-items-center">
	<div class="flex min-h-screen w-1/2 flex-col bg-gray-200 font-mono text-lg">
		<nav class="grid h-10 justify-center bg-red-700">
			<ul class="justify-item-center centent-center item-center grid grid-cols-3 justify-around">
				{@render nav_el({ name: 'HOME', url: '' })}
				{@render nav_el({ name: 'UPLOAD', url: 'upload' })}
				{@render nav_el({ name: 'HISTORY', url: 'history' })}
			</ul>
		</nav>
		<main class="flex-1">
			{@render children()}
		</main>
		<footer class="bg-red-700 p-4 text-center text-white">
			<div class="text-sm">
				<div class="grid content-center">© 2024 GD A7sen Fillier</div>
			</div>
		</footer>
	</div>
</div>
