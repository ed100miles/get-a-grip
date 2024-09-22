import { createCookieSessionStorage } from "@remix-run/node";

type SessionData = {
	userId: string;
	accessToken: string;
};

type SessionFlashData = {
	error: string;
};

const { getSession, commitSession, destroySession } =
	createCookieSessionStorage<SessionData, SessionFlashData>({
		cookie: {
			name: "__session",
			maxAge: 60,
			secure: true,
		},
	});

export { getSession, commitSession, destroySession };
