# Component Relevance Matrix + Layout Rules Matrix

## Component Relevance Matrix

| Component | dashboard | landing-page | auth-flow | settings | data-table | content-site | e-commerce | admin-panel |
|---|---|---|---|---|---|---|---|---|
| Button | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Input | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Card | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Badge | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Field | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Fieldset | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Form | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ |
| Select | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ |
| RadioGroup | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Table | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Sidebar | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Modal | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Tabs | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ❌ | ✅ |

**Rule:** Components marked ❌ are excluded from the project DESIGN.md. If a project has an unexpected need (e.g., a landing page with a signup form), use judgment — include Input + Field + Button if the landing page has a form. When in doubt, include rather than exclude.

## Layout Rules Matrix

| Layout pattern | dashboard | landing-page | auth-flow | settings | data-table | content-site | e-commerce | admin-panel |
|---|---|---|---|---|---|---|---|---|
| Sidebar (240px fixed) | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ |
| Hero section | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Feature sections | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| CTA section | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Centered card | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Single column | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Card grid | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Data table | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ |
| Filter bar | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| Section-based forms | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| Footer | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Content max-width: 1200px | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Content max-width: 720px | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Full-width | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Project Type Detection Keywords

| Type | Keywords in user request |
|---|---|
| dashboard | dashboard, analytics, admin panel, metrics, stats, KPI |
| landing-page | landing page, marketing page, product page, homepage, pitch |
| auth-flow | login, signup, register, sign in, onboarding, password reset |
| settings | settings, preferences, account, configuration, profile |
| data-table | table, list, inventory, CRUD, management, records |
| content-site | blog, docs, documentation, articles, knowledge base, content |
| e-commerce | shop, store, product catalog, cart, checkout, commerce |
| admin-panel | admin, CMS, internal tool, management, back office |