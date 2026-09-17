# Catalytic Souls Wiki (site)

A VitePress (Vite-powered) static wiki built from Tom Hughes' 2007 SIU Carbondale thesis and the research in `../research/`.

## Run locally

```bash
npm install
npm run dev
```

Then open http://localhost:5173. `npm run build` writes the static site to `docs/.vitepress/dist`; `npm run preview` serves that build.

## Deploy to Netlify

`netlify.toml` in this folder is already configured:

- Base directory: `site`
- Build command: `npm run build`
- Publish directory: `docs/.vitepress/dist`
- Node 22

Connect the repository in Netlify and point the site at the `site` subfolder (or drop this folder into Netlify Drop after running `npm run build` and uploading `docs/.vitepress/dist`).

## Structure

```
docs/
  .vitepress/config.mts   navigation, sidebar, search
  index.md                home
  timeline.md             master chronology 1969–2026
  thesis/                 summary + full text
  catalytic-souls/        crew, Underground Sound, Cave Fest, discography
  cave/                   venue history
  people/                 Tom Hughes and everyone else
  then-and-now/           scorecard + six topic pages (2007 → 2026)
  research/               method, findings log, raw agent reports
  public/flyers/          flyer images recovered from the Wayback Machine
```

Pages are plain Markdown; edit and rebuild. Local search is built in.
