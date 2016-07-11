import java.util.*;
import java.io.*;
import java.net.*;

public class Streamer {

	static long lastrun = 0;


	public static void main(String[] args) throws Exception {

		killLiveStreamer();
		updateChannels();
		launchLiveStreamer();


		Thread t = new Thread() {
			public void run() {
				while (true) {

					try {	
						Calendar c = Calendar.getInstance();
						long curr = c.getTimeInMillis();

						c.set(Calendar.HOUR_OF_DAY, 20);
						c.set(Calendar.MINUTE, 02);
						c.set(Calendar.SECOND, 00);
						c.set(Calendar.MILLISECOND, 00);

						if (curr > c.getTimeInMillis()) {
							c.add(Calendar.DATE, 1);
						}

						long wait = c.getTimeInMillis() - curr;

						System.out.println("Refreshing automatically in " + (wait / 1000.0 / 60.0 / 60.0) + " hrs...");
						Thread.sleep(wait);

						if (System.currentTimeMillis() - lastrun > 200000) {
							System.out.println("Refreshing channels...");
							killLiveStreamer();
							updateChannels();
							launchLiveStreamer();
						} else {
							System.out.println("Already refreshed manually, continue waiting...");
						}
					} catch (Exception e) {
						System.out.println("THREAD FAIL");
					}

				}
			}
		};

		t.start();

		while (true) {
			System.out.println("Waiting for refresh on port 7079...");
			ServerSocket ss = new ServerSocket(7079);
			Socket cs = ss.accept();

			updateChannels();
			killLiveStreamer();
			Thread.sleep(3000);
			launchLiveStreamer();
			ss.close();
			cs.close();
			Thread.sleep(30000);

		}



		}


		static private void updateChannels() throws Exception {
			Process p = Runtime.getRuntime().exec("python ustvnow.py");
			p.waitFor();
		}


		static private void killLiveStreamer() throws Exception {
			lastrun = System.currentTimeMillis();
			Process k = Runtime.getRuntime().exec("pkill -f livestreamer");
		}

		static private void launchLiveStreamer() throws Exception {

			ArrayList<String> links = new ArrayList<String>();
			File f = new File("Streams/USTV.txt");
			// File f = new File("Streams\\USTV.txt");
			Scanner sc = new Scanner(f);

			while (sc.hasNextLine()) {
				links.add(sc.nextLine());
			}

			Collections.sort(links);


			int port = 7070;
			int threads = 2;
			for (String link : links) {
				link = link.substring(link.indexOf(' ') + 1, link.length());
				System.out.println("adding: " + link);
				ProcessBuilder cspb = new ProcessBuilder("livestreamer", "-l", "debug", "--ringbuffer-size", "32M", "--player-external-http", "--stream-segment-threads", threads + "", "--player-external-http-port", port + "", link, "best");
				cspb.inheritIO();
				System.out.println("executing...");
				Process lv = cspb.start();
				port++;

			}

		}

	}





// ProcessBuilder cspb = new ProcessBuilder(MKVMERGE, "-o", tmp, x.recording); 	// run mkvmerge
// Process csp = cspb.start();
// csp.waitFor();