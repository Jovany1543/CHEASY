# CHEASY

## Frontend

The frontend uses React, React Router, and a flux-style store that is exposed to the app through context.

1. Start the Flask backend from `/workspaces/CHEASY/backend` on port `3001`.
2. From `/workspaces/CHEASY/frontend`, run `npm install`.
3. Start the frontend with `npm run start`.

The shared store and actions live in `frontend/src/store/flux.js`, and the provider is set up in `frontend/src/store/AppContext.js`.