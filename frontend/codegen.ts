import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
	schema: "../schema.graphql",
	generates: {
		"./gql/": {
			preset: "client",
			documents: ["gqlQueries/*.ts"],
			plugins: [],
		},
	},
};

export default config;
