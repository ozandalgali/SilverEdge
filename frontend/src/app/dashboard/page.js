import Card from '../ui/dashboard/card/card';
import styles from '../ui/dashboard/dashboard.module.css'
import Chart from '../ui/chart/chart';  
import WebSocketExample from '../ui/dashboard/websocket/websocket';


function Dashboard() {
    return (
        <div className={styles.wrapper}>
          <div className={styles.main}>
          <div className={styles.WebSocketExample}>
          <WebSocketExample />
         </div>
            <Chart />
          </div>
        </div>
    );
};

export default Dashboard;
