- [x] Testing

  - [x] setup a testing db
  - [x] setup api tests

- [x] Get userId from token in create pinches - else folk can guess other user ids and edit thier records

- [ ] Better signup

  - [ ] no duplicate usernames, emails
  - [ ] Email verification
  - [ ] Password reset
  🚫 User updates via the graphql? - no!
    - It's nice to allow gql access only to authed users, so create has to be outside, we dont want read / update / delete inside else it's messy. So keep all user management in the existing users route.

- [ ] Even better signup

  - [ ] SSO

- [ ] Build a frontend!

  - [ ] Create react app - that's it right?

- [ ] Deploy the app!
