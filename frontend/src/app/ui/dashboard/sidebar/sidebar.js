import styles from "./sidebar.module.css";
import Image from "next/image";
import MenuLink from "./MenuLink/menulink";
import { MdDashboard, MdShoppingCart, MdReceipt, MdPeople, MdLogout, MdSettings } from "react-icons/md";


const menuItems = [
    {
        title:"CEX",
        list: [{
            title: "Dashboard",
            path: "/dashboard",
            icon: <MdDashboard />
        },
        {
            title: "Products",
            path: "/dashboard/products",
            icon: <MdShoppingCart />
        },
        {
            title: "Rotator",
            path: "/dashboard/users",
            icon: <MdReceipt />
        },
        {
            title: "Customers",
            path: "/dashboard/transactions",
            icon: <MdPeople />
        },
        {
            title: "Settings",
            path: "/dashboard/settings",
            icon: <MdSettings />
        }]},
        {

        title:"Onchain Tools",
        list: [{
            title: "Wallet Tracker",
            path: "/wallettracker",
            icon: <MdDashboard />
        },
        {
            title: "Products",
            path: "/dashboard/products",
            icon: <MdShoppingCart />
        },
        {
            title: "Sniper",
            path: "/dashboard/users",
            icon: <MdReceipt />
        },
        {
            title: "Customers",
            path: "/dashboard/transactions",
            icon: <MdPeople />
        },
        {
            title: "Settings",
            path: "/dashboard/settings",
            icon: <MdSettings />
        }],
    },
]
function Sidebar() {
    return (
        <div className={styles.container}>
        <div className={styles.user}>
          <Image
            className={styles.userImage}
            src="/noavatar.png"
            alt=""
            width="50"
            height="50"
          />
          <div className={styles.userDetail}>
            <span className={styles.username}>Mochhi</span>
            <span className={styles.userTitle}>Administrator</span>
          </div>
        </div>
        <ul className={styles.list}>
          {menuItems.map((cat) => (
            <li key={cat.title}>
              <span className={styles.cat}>{cat.title}</span>
              {cat.list.map((item) => (
                <MenuLink item={item} key={item.title} />
              ))}
            </li>
          ))}
        </ul><br></br>
        <button className={styles.logout}>
            <MdLogout/>
            Logout</button>
        </div>
       
    )
};


export default Sidebar;