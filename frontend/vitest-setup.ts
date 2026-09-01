import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/svelte";
import { afterEach } from "vitest";

// @testing-library/svelte only registers cleanup itself when Vitest runs with
// `globals: true`. Without this, every rendered component stays mounted in
// document.body and a later test's query matches an earlier test's output.
afterEach(cleanup);
