import * as Dialog from '@radix-ui/react-dialog';
import { Link, Outlet, useLocation } from "@remix-run/react";
import { twMerge } from 'tailwind-merge';

const Home = () => {
    const location = useLocation();
    const is_login = location.pathname === "/home/login";
    return (
        <div className="flex flex-col items-center justify-center h-screen">
            <h1 className="text-4xl md:text-6xl font-bold text-white pb-5">👊 Get A Grip 👊</h1>
            <p className="text-white pb-5">The grip strength training app</p>
            <Dialog.Root>
                <Dialog.Trigger asChild>
                    <Link to={"/home/login"}>
                        <button type="button" className="bg-blue-700 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded mt-5">
                            Start Training
                        </button>
                    </Link>
                </Dialog.Trigger>
                <Dialog.Portal>
                    <Dialog.Overlay className="fixed bg-slate-900 inset-0 opacity-85 data-[state=open]:animate-overlayShow" />
                    <Dialog.Content className="data-[state=open]:animate-contentShow fixed top-[50%] left-[50%] max-h-[85vh] w-[90vw] max-w-[450px] translate-x-[-50%] translate-y-[-50%] rounded-[6px] bg-white shadow focus:outline-none border-2 border-white overflow-auto">
                        <div className="flex w-full rounded-md">
                            <Link to="/home/login" className={twMerge(
                                "basis-1/2 text-center rounded-tl-md p-1 border-b-2",
                                is_login ?
                                    "bg-slate-900 text-white"
                                    : "bg-gray-300 text-slate-900"

                            )}>Login</Link>
                            <Link to="/home/register" className={twMerge(
                                "basis-1/2 text-center rounded-tr-md p-1 border-b-2",
                                !is_login ?
                                    "bg-slate-900 text-white"
                                    : "bg-gray-300 text-slate-900"

                            )}>Register</Link>
                        </div>
                        <div className="bg-slate-900 p-5" >
                            <Outlet />
                        </div>
                    </Dialog.Content>
                </Dialog.Portal>
            </Dialog.Root >
        </div>
    );
}

export default Home;
