<script>
	import axios from 'axios';
	let avatar, fileinput, imsrc;
	let text = 'Upload';
	let ready = true;
	const onFileSelected = (e) => {
		let image = e.target.files[0];
		let reader = new FileReader();
		reader.readAsDataURL(image);
		reader.onload = (e) => {
			avatar = image;
			imsrc = e.target.result;
		};
	};

	async function GetUrl() {
		try {
			const response = await fetch('http://localhost:8080/url');

			if (!response.ok) {
				throw new Error('Error 504 : could not fetsh the url');
			}
			const url = await response.json();
			return url.url;
		} catch (error) {
			console.log(error);
		}
	}

	async function UploadImage(param) {
		if (param == undefined) {
			console.error('No image provided for upload.');
			return;
		}

		// Create FormData and append the image
		const formData = new FormData();
		formData.append('image', param);
		console.log(formData.get('image'));

		let url;

		try {
			const generatedUrl = await GetUrl();
			console.log(generatedUrl);

			url = `http://localhost:8080/upload/${generatedUrl}`;
			console.log(`Upload URL generated: ${url}`);
		} catch (error) {
			console.error('Error while generating the upload URL:', error);
			return;
		}

		try {
			// Perform the upload
			const response = await axios.post(url, formData, {
				headers: {
					'Content-Type': 'multipart/form-data'
				}
			});

			console.log('Image uploaded successfully. Server response:', response.data);
			// Assuming 'text' is defined elsewhere in your context
			text = 'Processing';
		} catch (error) {
			console.error('Failed to upload the image:', error.message);
			console.debug('Full error details:', error);
		}
	}
</script>

<div id="app">
	<h1>Upload Image</h1>

	{#if avatar}
		<img class="avatar" src={imsrc} alt="d" />
	{:else}
		<img
			class="avatar"
			id="image"
			src="https://cdn4.iconfinder.com/data/icons/small-n-flat/24/user-alt-512.png"
			alt=""
		/>
	{/if}
	<img class="upload" src="https://static.thenounproject.com/png/625182-200.png" alt="" />
	<div
		class="chan"
		role="button"
		aria-pressed="false"
		tabindex="0"
		on:click={() => {
			fileinput.click();
		}}
		on:keydown={(e) => {
			if (e.key === 'Enter' || e.key === 'Space') {
				fileinput.click();
			}
		}}
	>
		Choose Image
	</div>
	<input
		style="display:none"
		type="file"
		accept=".jpg, .jpeg, .png"
		on:change={(e) => onFileSelected(e)}
		bind:this={fileinput}
	/>
	<dev
		class="mt-10 cursor-pointer border-2 border-gray-800 p-2"
		role="button"
		aria-pressed="false"
		tabindex="0"
		on:click={() => {
			UploadImage(avatar);
		}}
		on:keydown={(e) => {
			if (e.key === 'Enter') {
				UploadImage(avatar);
			}
		}}
	>
		{text}
	</dev>
	<dev
		class="mt-10 cursor-pointer border-2 border-gray-800 p-2"
		role="button"
		aria-pressed="false"
		tabindex="0"
		on:click={() => {
			window.location.href = '/prediction';
		}}
		on:keydown={(e) => {
			if (e.key === 'Enter') {
				window.location.href = '/prediction';
			}
		}}
	>
		See Prediction
	</dev>
</div>

<style>
	#app {
		display: flex;
		align-items: center;
		justify-content: center;
		flex-flow: column;
	}

	.upload {
		display: flex;
		height: 50px;
		width: 50px;
		cursor: pointer;
	}
	.avatar {
		display: flex;
		height: 200px;
		width: 200px;
	}
</style>
