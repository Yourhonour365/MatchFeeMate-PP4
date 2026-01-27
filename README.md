## Design

### Wireframes

Wireframes were created using [Balsamiq](https://balsamiq.com/) following a mobile-first approach, reflecting the primary use case of captains managing their team from their phone at the cricket ground.

#### Landing Page

| Mobile | Desktop |
|--------|---------|
| ![Landing page mobile](docs/readme/wireframes/wireframe_landing_mobile.png) | ![Landing page desktop](docs/readme/wireframes/wireframe_landing_desktop.png) |

#### Authentication

| Login | Sign Up |
|-------|---------|
| ![Login](docs/readme/wireframes/wireframe_login.png) | ![Sign up](docs/readme/wireframes/wireframe_signup.png) |

#### Players

| Player List | Player Form |
|-------------|-------------|
| ![Player list](docs/readme/wireframes/wireframe_player_list.png) | ![Player form](docs/readme/wireframes/wireframe_player_form.png) |

#### Matches

| Match List | Match Detail | Match Form |
|------------|--------------|------------|
| ![Match list](docs/readme/wireframes/wireframe_match_list.png) | ![Match detail](docs/readme/wireframes/wireframe_match_detail.png) | ![Match form](docs/readme/wireframes/wireframe_match_form.png) |

*The match detail screen is the operational hub - showing availability at a glance with colour-coded status indicators, and providing direct access to both availability management and team selection.*

#### Opposition

| Opposition List | Opposition Form |
|-----------------|-----------------|
| ![Opposition list](docs/readme/wireframes/wireframe_opposition_list.png) | ![Opposition form](docs/readme/wireframes/wireframe_opposition_form.png) |

#### Team Selection

![Team selection](docs/readme/wireframes/wireframe_team_selection.png)

*Team selection shows only available players, with a running count of selections against the required 11.*

---

### User Flows

User flow diagrams were created to map the key journeys through the application. Grey rounded rectangles indicate handoffs to other flows.

#### Authentication Flows

| Sign Up | Login |
|---------|-------|
| ![Sign up flow](docs/readme/userflows/flow_signup.png) | ![Login flow](docs/readme/userflows/flow_login.png) |

#### Club Management

![Club flow](docs/readme/userflows/flow_club.png)

*New users are prompted to either join an existing club or create a new one.*

#### Core Management Flows

| Players | Opposition | Matches |
|---------|------------|---------|
| ![Player flow](docs/readme/userflows/flow_player.png) | ![Opposition flow](docs/readme/userflows/flow_opposition.png) | ![Match flow](docs/readme/userflows/flow_match.png) |

#### Match Day Flows

| Availability | Team Selection |
|--------------|----------------|
| ![Availability flow](docs/readme/userflows/flow_availability.png) | ![Selection flow](docs/readme/userflows/flow_selection.png) |