- [x] Testing

  - [x] setup a testing db
  - [x] setup api tests

- [x] Get userId from token in create pinches - else folk can guess other user ids and edit thier records

- [ ] Better signup

  - [x] no duplicate usernames, emails - i think duplicate username should be ok?
  - [x] Email verification
  - [ ] resend verification email
  - [x] unvalidated users cant login
  - [x] Jinja template for email verification
  - [ ] Password reset
        🚫 User updates via the graphql? - no! - It's nice to allow gql access only to authed users, so create has to be outside, we dont want read / update / delete inside else it's messy. So keep all user management in the existing users route.

- [ ] Even better signup

  - [ ] SSO

- [ ] Add logger

- [ ] Handle database migrations

- [ ] Build a frontend!

  - [x] Remix basic setup
  - [x] Signup flow
  - [x] Login
  - [ ] Logout
  - [ ] Dashboard
  - [ ] Add a pinch
  - [ ] View pinches data viz

- [ ] Deploy the app!
