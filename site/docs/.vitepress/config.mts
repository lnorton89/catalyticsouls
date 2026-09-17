import { defineConfig } from 'vitepress'

export default defineConfig({
  // GitHub Pages serves the site under /<repo>/; Netlify or a custom domain would use '/'.
  base: process.env.VITEPRESS_BASE || '/catalyticsouls/',
  title: 'Catalytic Souls Wiki',
  description:
    'Tom Hughes’ 2007 SIU thesis on electronic dance music, the Catalytic Souls crew, Underground Sound, and the Shawnee Salt Petre Cave, brought up to date through 2026.',
  lang: 'en-US',
  lastUpdated: false,
  cleanUrls: true,
  head: [
    ['link', { rel: 'icon', href: (process.env.VITEPRESS_BASE || '/catalyticsouls/') + 'favicon.svg', type: 'image/svg+xml' }],
    ['meta', { name: 'theme-color', content: '#c2410c' }]
  ],
  themeConfig: {
    siteTitle: 'Catalytic Souls',
    nav: [
      { text: 'The Thesis', link: '/thesis/' },
      { text: 'Catalytic Souls', link: '/catalytic-souls/' },
      { text: 'The Cave', link: '/cave/' },
      { text: 'Then & Now', link: '/then-and-now/' },
      { text: 'Timeline', link: '/timeline' },
      { text: 'Media', link: '/media' },
      { text: 'Research', link: '/research/' }
    ],
    sidebar: [
      {
        text: 'Start here',
        items: [
          { text: 'Overview', link: '/' },
          { text: 'Master timeline 1969–2026', link: '/timeline' },
          { text: 'Video & flyer archive', link: '/media' }
        ]
      },
      {
        text: 'The Thesis (2007)',
        items: [
          { text: 'What the thesis is and argues', link: '/thesis/' },
          { text: 'Full text', link: '/thesis/full-text' }
        ]
      },
      {
        text: 'Catalytic Souls',
        items: [
          { text: 'The crew', link: '/catalytic-souls/' },
          { text: 'Underground Sound 1–7', link: '/catalytic-souls/underground-sound' },
          { text: 'Cave Fest & CaveStock', link: '/catalytic-souls/cave-fest-cavestock' },
          { text: 'Label & discography', link: '/catalytic-souls/discography' }
        ]
      },
      {
        text: 'The Cave',
        items: [{ text: 'Shawnee Salt Petre Cave, 1969–2026', link: '/cave/' }]
      },
      {
        text: 'People',
        items: [
          { text: 'Tom Hughes / TomFoolery', link: '/people/tom-hughes' },
          { text: 'Everyone else', link: '/people/' }
        ]
      },
      {
        text: 'Then & Now (2007 → 2026)',
        items: [
          { text: 'Reading the thesis in 2026', link: '/then-and-now/' },
          { text: 'Scorecard: claims vs. outcomes', link: '/then-and-now/scorecard' },
          { text: 'Vinyl, downloads & retail', link: '/then-and-now/vinyl-and-retail' },
          { text: 'Beatport & distribution', link: '/then-and-now/beatport-and-distribution' },
          { text: 'The EDM boom and bust', link: '/then-and-now/boom-and-bust' },
          { text: 'Law & media', link: '/then-and-now/law-and-media' },
          { text: 'DJ & production technology', link: '/then-and-now/technology' },
          { text: 'Scholarship', link: '/then-and-now/scholarship' }
        ]
      },
      {
        text: 'Research',
        items: [
          { text: 'Method, sources & open questions', link: '/research/' },
          { text: 'Primary findings log', link: '/research/findings-log' },
          { text: 'Agent report: the crew', link: '/research/agent-report-crew' },
          { text: 'Agent report: the venue', link: '/research/agent-report-venue' },
          { text: 'Agent report: the industry', link: '/research/agent-report-industry' }
        ]
      }
    ],
    search: { provider: 'local' },
    outline: { level: [2, 3] },
    footer: {
      message:
        'A research wiki built from Thomas W. Hughes’ 2007 SIU Carbondale thesis and public sources. Not affiliated with SIU, Full Sail, or the Shawnee Cave Amphitheater.',
      copyright: 'Compiled September 2026.'
    },
    docFooter: { prev: 'Previous', next: 'Next' }
  }
})
