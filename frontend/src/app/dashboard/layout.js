import Head from "next/head";
import Sidebar from "../ui/dashboard/sidebar/sidebar";
import Navbar from "../ui/dashboard/navbar/navbar";

const Layout = ({children}) => (
    (
        <div>
            <Head>
                <title>SilverEdge</title>
            </Head>
            <div>
                <Sidebar />
            </div>
            <div>
                <Navbar />
                {children}
            </div>
        </div>
    )
);

export default Layout;