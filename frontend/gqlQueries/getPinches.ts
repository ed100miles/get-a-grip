import { graphql } from "../gql";

const GetPinches = graphql(`
    query GetPinches($userId: Int!, $createdAfter: DateTime, $createdBefore: DateTime, $wide: Boolean, $deep: Boolean, $minWeight: Float, $maxWeight: Float, $minDuration: Float, $maxDuration: Float) {
        pinches(userId: $userId createdAfter: $createdAfter createdBefore: $createdBefore wide: $wide deep: $deep minWeight: $minWeight maxWeight: $maxWeight minDuration: $minDuration maxDuration: $maxDuration) {
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
