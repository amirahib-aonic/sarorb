# Deployment

Live prototype for judges: https://ignis-borneo.vercel.app

- Vercel project `ignis-borneo` in the team "Legesus' projects".
- Static site: `docs/research/prototypes/borneo.PROTOTYPE.html` served as `index.html`, plus `borneo.PROTOTYPE.data.js`. No build step.
- Deployed by upload, not Git, because the repo's GitHub account does not have the Vercel GitHub app installed. Redeploy with the `deploy-prototype` project skill, which builds the bundle with `scripts/build-prototype-deploy.sh`.
- First deployed 14 Nov 2026 from commit `6c3d366`.
