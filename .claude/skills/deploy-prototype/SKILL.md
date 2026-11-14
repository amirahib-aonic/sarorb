---
name: deploy-prototype
description: Deploy the IGNIS Borneo prototype (docs/research/prototypes/borneo.PROTOTYPE.html) to the personal Vercel project ignis-borneo at https://ignis-borneo.vercel.app. Use when the user asks to deploy, redeploy, publish or update the live prototype, or to check what version is live.
---

# Deploy the prototype

The live site is the Vercel project **ignis-borneo** in the team **Legesus' projects** (`team_gOXaTfd9qCIcYEHeqhEdxuo9`), served at https://ignis-borneo.vercel.app. It is a static page: `index.html` (a copy of `borneo.PROTOTYPE.html`) plus `borneo.PROTOTYPE.data.js`. There is no build step.

The project is **not linked to Git**. The repo `amirahib-aonic/sarorb` belongs to a colleague, and the Vercel GitHub app is not installed on that account, so `create_git_project` fails with "install the GitHub integration first". Every deploy is a manual upload. Amirah's own Vercel project for the same repo is separate; nothing here touches it.

## Steps

1. **Check the source.** Deploy from `adam-dev` with the prototype files committed. Run `git status --short docs/research/prototypes`; if it shows changes, say so and ask whether to deploy uncommitted work.
2. **Build the bundle.** Run `sh scripts/build-prototype-deploy.sh`. It writes `.deploy/ignis-borneo.zip` (index.html + data file) and `.deploy/REVISION` with the commit it came from. `.deploy/` is gitignored.
3. **Upload with BrowserOS neo** (the user is signed in to Vercel there):
   - Open `https://vercel.com/new`, click **Choose a file to deploy**, and upload the zip with `page.upload(null, [<absolute path to .deploy/ignis-borneo.zip>])`. The folder chooser does not accept a directory path; the zip works.
   - On the "Drop to Deploy" page, click **Deploy to an existing project instead**, pick **ignis-borneo**, then **Deploy**. Do not create a second project.
4. **Verify.** Open https://ignis-borneo.vercel.app and wait for the text "Burning Calendar"; confirm "All of Borneo" appears. Use the Vercel MCP `list_deployments` / `get_deployment` with the team id above if the build state is unclear.
5. **Report** the URL and the revision from `.deploy/REVISION`.

## Rules

- Never push or change Git settings as part of a deploy. Pushing needs the user's explicit yes.
- The site is public. Before deploying, confirm the bundle holds only the two files above, with no personal data.
- The Vercel MCP `upload_file` tool needs file contents passed inline, which is too large for the 2.2 MB data file. Use the browser upload.

## Switching to Git deploys later

If the Vercel GitHub app is installed on `amirahib-aonic` (only the repo owner can do this), link instead: Vercel MCP `create_git_project` with `repo: amirahib-aonic/sarorb`, `rootDirectory: docs/research/prototypes`, then `update_project` and set the production branch to `adam-dev` in the project settings. Then rewrite this skill around pushes.
