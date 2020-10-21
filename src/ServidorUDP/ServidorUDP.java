package ServidorUDP;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.nio.ByteBuffer;
import java.util.zip.CRC32;
public class ServidorUDP {
	private DatagramSocket udpSocket;
	private int port;

	public ServidorUDP(int port) throws SocketException, IOException {
		this.port = port;
		this.udpSocket = new DatagramSocket(this.port);
	}
	private void send() throws Exception {
		System.out.println("-- Running Server at " + InetAddress.getLocalHost() + "--");

		byte[] data = new byte[256];
		ByteBuffer b = ByteBuffer.wrap(data);
		File file = new File("./");
		FileInputStream fis = new FileInputStream(file);
		BufferedInputStream bis = new BufferedInputStream(fis);
		CRC32 crc = new CRC32();

		while(true) {
			b.clear();
			b.putLong(0);
			int bytesRead = bis.read(data, 8, data.length-8);
			if(bytesRead == -1)
				break;
			crc.reset();
			crc.update(data, 8, data.length-8);
			long chksum = crc.getValue();
			b.rewind();
			b.putLong(chksum);
			DatagramPacket p = new DatagramPacket(data, 256);
			
			this.udpSocket.send(p);  
		}
		bis.close();
		fis.close();
	}

	public static void main(String[] args) throws Exception {
		ServidorUDP client = new ServidorUDP(7077);
		client.send();
	}
}
