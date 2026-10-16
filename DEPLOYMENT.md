# Static deployment

The built `public/` directory is ready to serve. Research Python never runs during deployment. Do not configure a Python or Next.js project.

## Vercel dashboard

1. Put the contents of this project in a new GitHub repository you control. Do not upload the outer ZIP itself as a repository file.
2. Import that repository into Vercel. Set Framework Preset to **Other** and Root Directory to the project root.
3. The checked-in `vercel.json` specifies `public` as output. Its install/build commands only echo a message: all assets already exist.
4. If privacy is required, configure Deployment Protection for the intended deployment **before sharing or promoting it**. Confirm your account/plan supports the desired protection. The configuration file alone does not provide authentication.
5. Deploy and check `/`, figures, citations, maths and the optional educational controls on desktop/mobile.

## Vercel CLI

With Vercel CLI installed and your account authenticated:

```bash
vercel
```

This creates a preview deployment. Confirm its access protection in Vercel. Use `vercel --prod` only when you intend production publication and the audience is correct. No Vercel account was connected in this task and no Vercel deployment was executed here.

## Local check

```bash
python scripts/check_site.py
python -m http.server 8000 --directory public
```

The project also includes a private ChatGPT Sites deployment when deployment succeeds. That is separate from Vercel; see the final delivered URL. The `.openai` hosting configuration is specific to that private deployment and is not needed by Vercel.

Configuration references checked during implementation:
- https://vercel.com/docs/project-configuration/vercel-json
- https://vercel.com/docs/deployment-protection
