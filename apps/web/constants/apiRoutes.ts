/**
 * API Routes Configuration for the Frontend (Next.js).
 * This file centralizes API path management by reading the backend's source-of-truth
 * from the shared `apiRoutes.json` and prepending the '/api' proxy prefix
 */

import routes from "@common/apiRoutes.json";

type ApiRoutes = typeof routes;

// Process the raw routes to create the final, frontend-ready API paths.
const API_ROUTES_FRONTEND: ApiRoutes = Object.fromEntries(
  Object.entries(routes).map(([key, path]) => [key, `/api${path}`]) //convert json into an array
) as ApiRoutes;

export const API_ROUTES = API_ROUTES_FRONTEND;
