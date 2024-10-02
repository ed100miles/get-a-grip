import { graphql } from "../gql";

const GetPinches = graphql(`
    query GetPinches($userId: Int!) {
        pinches(userId: $userId) {
            id
            userId
            wide
            deep
            weight
            duration
            createdAt
        }
    }
`);

export default GetPinches;
