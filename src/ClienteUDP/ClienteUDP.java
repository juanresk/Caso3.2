package ClienteUDP;

import java.io.File;
import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.util.Scanner;

public class ClienteUDP {
	private DatagramSocket udpSocket;
	private String serverAddress;
	private int port;
	private Scanner scanner;
	private ClienteUDP(String destinationAddr, int port) throws IOException {
		this.serverAddress = destinationAddr;
		this.port = port;
		InetSocketAddress address = new InetSocketAddress(serverAddress, this.port);
		udpSocket = new DatagramSocket(null);
		udpSocket.bind(address);
	}
	public static void main(String[] args) throws NumberFormatException, IOException {        
		ClienteUDP sender = new ClienteUDP("192.168.0.22", 7077);
		System.out.println("-- Running UDP Client at " + sender.serverAddress + " --");
		sender.listen();
	}
	private void listen() throws IOException {
		byte[] buf = new byte[256];
		while(true) {
			DatagramPacket packet = new DatagramPacket(buf, buf.length);
			// blocks until a packet is received
			udpSocket.receive(packet); 
			String msg;
			msg = new String(packet.getData()).trim();

			System.out.println(
					"Message from " + packet.getAddress().getHostAddress() + ": " + msg);
		}
	}
}