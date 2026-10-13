# Product

Status: proposed

## Product vision

For groups of friends in London, it is difficult to find the best venue. It's difficult to work out the best location for everyone to travel to. It's difficult to know good venues in these locations. It adds friction to people spending time together. Currently, there is no service for groups that helps with this. PubPoint will fill that gap. This problem is much harder in large cities like London, where public transport can mean that the most equal or best-located venue will not always be in the middle of the group in terms of geographic centre. PubPoint will suggest the best and fairest venue for them to travel to. Eventually, it will allow them to filter for things they want, like dog-friendly, pub garden, kitchen open now, and good cocktails. Our market is people living in large cities with complex travel networks who want to spend time with their friends or family.

## Problem and opportunity

- What problem or need are users experiencing?
  Groups of friends struggle to find venues that are well located for everyone in the group and hit all the criteria they're looking for.
- How do they handle it today?
  Currently, people spend lots of time in group chats discussing their current locations, discussing venues they know that are good, researching the venue and negotiating with each other about where they will be going.
- What makes solving it worthwhile?
  Friends will love reducing friction in choosing places to meet up. They'll spend more time together, go to better venues, and have better times.

## Target users

This problem is much greater for people and groups in cities with complicated transport networks: large cities like London, Tokyo, Paris, Singapore. The people I envisage using the app are social people: people that want to hang out with their friends and people who want to associate with the brand. I think initially I see this for people who are social, younger people who are tech-savvy and want to spend more time with their friends.

## MVP outcomes and success

### User outcomes

- A group can find and agree on a pub or bar in London that works for its members' starting locations and transport choices.
- Members can understand the travel tradeoffs between venue options and decide whether the suggested venue works for them.
- The group can spend less effort choosing where to meet than it would through its usual group chat discussion.

## MVP scope

Tracks an initial list of things that we want the product to do and, more critically, things we do not need the product to do at this stage.

### In scope

- Account creation and sign-in
- Group creation and management
- Group invitations by email or phone, with membership granted on acceptance
- Guest participants in searches, with optional invitations that link them to an account and grant group and originating-search access
- Flexible groups, which act as the starting point of searches but allow dynamic adjustment
- Flexible user state for searches, where the home address, work address, custom address, or current location can be easily swapped by any member within their search
- Minimal-friction method to amend groups for or create ad hoc searches
- Searching for and comparing pubs or bars for a group
- Persistent user home address and transport settings
- Viewing travel information and opening external route planners

### Out of scope

- Recent people lists based on previous groups or searches
- Friends lists and friendship requests
- Guest membership in saved groups
- Filtering venues based upon characteristics you want (e.g., pub garden, kitchen, open late, dog friendly)
- Sorting venues based upon their ratings
- Ability for venues to boost their place within our ranking algorithm
- Allowing users to change preferences for the search algorithm (e.g., one person is happy to travel further, dislike certain areas)
- Group-specific default starting location for a user - just have a default on the user level
- Venues other than pubs or bars
- Route finding in app
- Live venue information
- Suggesting alternative efficient transport methods for different users in a group to a venue (E.g., it would be faster to walk than take the bus to a venue.)
- Allowing multiple possible transport types for a user in a given search
- Sophisticated algorithmic biasing of the search results to give varied alternative venue options to the users
- Have functionality for a meeting time and sending a notification to the user with their travel information when they need to leave.

## User journeys

The following section covers the main user journeys for the MVP. Detailed user flows can be documented separately and linked from here. Technical design belongs in [`development/`](development/).

Actions describe the user's steps; variations describe alternative paths to that outcome. System capabilities describe the responsibilities needed to make the journey possible, with technical design recorded in [`development/`](development/).

### Sign up and get started

**Scenario:** A new user creates an account and sets initial search defaults so they are ready to use PubPoint.

**Starting conditions:** The person does not yet have a PubPoint account.

**User actions**

1. Provide the details needed to create an account.
2. Set an initial home address and default transport type.
3. Continue to finding a venue or saving a group.

**Successful outcome:** The user has an account they can return to, with any supplied defaults available for searches.

**Variations**

- A returning user signs in to their existing account and uses their saved settings and groups.
- A person arriving through an invitation signs up or signs in, then continues to [accept the invitation](#accept-a-group-invitation-and-join-a-search).

**System capabilities required**

- Create and retain a user account, validating the supplied account details.
- Authenticate returning users and identify whose settings and groups to make available.
- Store initial search defaults through the capabilities described in [Update personal search defaults](#update-personal-search-defaults).

### Find a venue for a meetup

**Scenario:** A person starts a search from a saved group or an ad hoc set of participants, adjusts their starting locations and transport choices, and compares suggestions to choose a suitable pub or bar.

**Starting conditions:** The person knows who they want to include and can access the saved group if using one.

**User actions**

1. Select a saved group or start an ad hoc search without first saving a group.
2. Add or remove participants for the search with minimal steps. Include someone without an account as a guest by supplying a name, starting location, and optional transport choice; contact details for an optional group invitation can be added later.
3. Choose a starting location for yourself or another participant: home address, work address, custom address, or available shared current location. Adjust a location by dragging it on the group map or entering an address or venue name.
4. Review or change each participant's transport type, with one transport type per participant.
5. Search for pubs or bars, cycle through the options, and compare travel information for each participant.
6. Choose a suitable venue and, if needed, open Google Maps, Citymapper, or Apple Maps for directions.

**Successful outcome:** The person has found a suitable venue and can understand each participant's journey from their chosen starting location.

**Variations**

- Start from a saved group, using its membership and members' personal defaults, or build the participant list ad hoc.
- Change participants, starting locations, or transport choices and search again when plans change.
- Continue to [Create and manage a reusable group](#create-and-manage-a-reusable-group) to retain accepted members for reuse. Guests stay in the current search.
- Optionally enter a guest's email address or phone number and invite them to the saved group associated with the search. Show their invitation as pending while they continue to participate as a guest.
- For an ad hoc search, create a saved group before sending group invitations.

**System capabilities required**

- Initialise a search from saved group membership and user settings, or from participants selected ad hoc.
- Track the participants, starting locations, and transport choices for each search separately from saved groups and user settings.
- Represent registered users and guests as search participants, including guests who have not signed up or completed onboarding.
- Include guests in recommendations and travel comparisons without requiring contact details or invitation acceptance.
- Link a guest's optional invitation to the saved group and their entry in the originating search, keeping the guest entry usable while the invitation is pending.
- Allow any group member preparing a search to adjust the participants and their starting locations within that search, and accept transport changes for the search.
- Make location adjustments available to other group members involved in the search. The timing, confirmation, and handling of parallel searches remain open collaboration questions.
- Resolve entered addresses and venue names, map selections, and available shared current locations to starting points usable for venue searches.
- Support switching between location choices and identify missing or unusable location or transport information before running the search.
- Maintain pub and bar information sufficient to find candidate venues.
- Use the current search inputs to estimate travel times and recommend venues suitable for the group.
- Provide alternative venues and comparable travel information for each participant, including changes made by another member.
- Update suggestions when the user runs a search with changed inputs.
- Generate external route-planner links using the participant's search starting location and selected venue destination.

### Create and manage a reusable group

**Scenario:** A person creates or opens a saved group, manages its membership, and invites people so the group can be reused for future searches. They can do this directly or start from participants in a current search.

**Starting conditions:** The person is signed in. Updating an existing group requires permission to manage it.

**User actions**

1. Open the Groups page and create a group or select an existing group. Alternatively, start from participants in a current search.
2. Review accepted members and pending invitations.
3. Enter an email address or phone number to invite someone, whether or not they already have a PubPoint account.
4. Manage members and invitations, including removing members or cancelling invitations when authorised. Members can leave the group.
5. Retrieve the group when starting a future search.

**Successful outcome:** The saved group contains registered users who have accepted membership, with outstanding invitations shown separately. Future searches use members' user-level starting-location defaults.

**Variations**

- Create and manage a group directly on the Groups page without running a venue search.
- Update the membership of the group a search started from, or save the adjusted registered participants as a new group. Retain existing accepted memberships and invite anyone who has not accepted membership of the destination group.
- When saving from a search, leave guests in the current search and explain that they are excluded from saved membership. Optionally invite them to join the group.

**System capabilities required**

- Associate users with groups and determine who belongs to each group.
- Save, retrieve, and manage reusable groups through a dedicated group management page.
- Send group invitations by email or phone to existing users or people without an account.
- Track accepted memberships and pending invitations separately; grant new membership only after acceptance.
- Treat creating a group as the creator's acceptance of membership, with the location-sharing behavior explained before creation.
- Support authorised membership removal and invitation cancellation, and allow members to leave.
- Identify the group a search started from so an authorised user can explicitly update its membership or invite additional search participants.
- Create a new saved group directly or from current search participants, with registered users joining through invitation acceptance and guests excluded from saved membership until they register and accept.
- Use members' user-level starting-location defaults when the group is used for a new search.

### Accept a group invitation and join a search

**Scenario:** An invited person accepts membership of a saved group. If the invitation came from their guest entry in a search, their account replaces that entry and they gain access to the originating search.

**Starting conditions:** The person has a pending invitation to a saved group, optionally linked to a guest participant in a current search.

**User actions**

1. Open the invitation received by email or phone.
2. Sign up or sign in to the intended account.
3. Review the group, its members, and the location-sharing behavior, then accept or decline the invitation.
4. On acceptance, open the group and, when invited from a guest entry, join the originating search.

**Successful outcome:** The person is an accepted group member. Their account replaces any linked guest entry, preserving that search's starting location and transport choice.

**Variations**

- An existing user signs in; a new user completes signup.
- An invitation from group management grants group membership without requiring an existing search.
- A declined invitation leaves the person outside the saved group and any guest entry in the search unchanged.

**System capabilities required**

- Associate the invitation with its intended recipient, destination group, and any originating guest entry and search.
- Let the recipient accept or decline after signing up or signing in, and apply acceptance only to a valid pending invitation.
- Grant group membership and its location access on acceptance.
- Replace the linked guest entry with the accepting account, preserving the search inputs and avoiding a duplicate participant if that account is already in the search.
- Grant the accepting user access to the originating search when the invitation is linked to their guest entry.
- Keep the guest's search inputs separate from the accepting user's personal defaults.

### Update personal search defaults

**Scenario:** A user changes their saved home address or transport preference so future searches start with the appropriate defaults.

**Starting conditions:** The user is signed in to their account.

**User actions**

1. Open personal settings and review the saved home address and default transport type.
2. Set or change either value and save the changes.
3. Start a future search using the updated defaults, adjusting them within that search when needed.

**Successful outcome:** The user's saved defaults reflect their choices and are available for subsequent searches.

**Variations**

- Set a home address for the first time or update an existing address.
- Change only the address, only the transport type, or both.

**System capabilities required**

- Save and retrieve each user's home address and default transport type.
- Resolve the home address to a location usable for venue searches.
- Validate changes and report when an address or transport choice cannot be used.
- Make members' addresses and default transport settings available when preparing a search.
- Make updated settings available as defaults for subsequent searches.

## Shared product requirements

- **Address sharing:** Creating a group or accepting a group invitation shares the user's home address with current and future accepted members of that group. The app makes this clear before creation or acceptance. Joining another person's group requires invitation acceptance for that group.
- **Guests and invitations:** Guests participate in searches without an account. They become saved group members only after signing up or signing in and accepting the invitation. Pending invitations do not grant membership or access to members' saved addresses.
- **Access:** Users can only view or change information they are authorised to access, including account settings and groups.
- **Supported devices:** Users can complete the MVP journeys on mobile and desktop. TBC
- **Feedback and errors:** The app clearly shows when an action is processing, whether it succeeded, and what the user can do if it fails. A failed search preserves the user's selections so they can retry.
- **Saved information:** Saved groups and account settings remain available when a user returns to the app.

## Assumptions and open questions

- Review privacy, security, and data handling for sharing addresses with current and future group members and linking guest entries to accounts. The MVP sharing behavior above is a product decision; this review remains open.
- Who can invite or remove members and cancel invitations within a group?
- How long do pending invitations and their originating searches remain available, and what happens if the originating search ends before acceptance?
- Which sign-up and sign-in method should the MVP support, and when must a new user supply an initial home address and transport type?
- Decide whether to build a web or app frontend first.
- Should users also be able to explicitly save search-specific changes back to their own user settings?
- Should work addresses be saved in user settings or entered when preparing a search?
- How is a member's current location shared for a search: as a one-off starting point or as a continuously updated live location? I assume there are big data privacy and safety concerns with this.
- What travel information should users see within the app, beyond estimated journey times?
- A key thing to finalise is the level of collaboration on a search. Are searches real-time on everyone's phone, and can you see instant updates that other people make to a particular search? How do users start parallel searches for each other at the same time for a specific group? Do users need to opt in for a search? Do users need to accept a location change for a search? Will other members see the current preferred venue option for a particular member? How is this current preferred choice shared between the members?
- The granularity/accuracy acceptable for our journey time
- Further tighten up the approach around guest members on a search, inviting unauthenticated members to be this guest member and group membership.
