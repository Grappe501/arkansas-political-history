/// <reference types="@sveltejs/kit" />
/// <reference types="vite/client" />

// Allow JSON imports (e.g. generated indexes)
declare module '*.json' {
	const value: any;
	export default value;
}

// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
