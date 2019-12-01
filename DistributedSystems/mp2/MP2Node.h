/**********************************
 * FILE NAME: MP2Node.h
 *
 * DESCRIPTION: MP2Node class header file
 **********************************/

#ifndef MP2NODE_H_
#define MP2NODE_H_

/**
 * Header files
 */
#include "stdincludes.h"
#include "EmulNet.h"
#include "Node.h"
#include "HashTable.h"
#include "Log.h"
#include "Params.h"
#include "Message.h"
#include "Queue.h"
#include <list>

#define NUM_KEY_REPLICAS 3
#define QUORUM_COUNT ((NUM_KEY_REPLICAS)/2+1)
#define RESPONSE_WAIT_TIME 20
/**
 * CLASS NAME: MP2Node
 *
 * DESCRIPTION: This class encapsulates all the key-value store functionality
 * 				including:
 * 				1) Ring
 * 				2) Stabilization Protocol
 * 				3) Server side CRUD APIs
 * 				4) Client side CRUD APIs
 */

/* Custom message wrapper needed for replicate messages */
class MyMessage:public Message{
    public:
		enum MyMessageType { REPUPDATE, QUERY };
		string toString();
		static string getMsg(string message); 
		MyMessage(MyMessageType type, string msg);
		MyMessageType msgType;
		MyMessage(MyMessageType type, Message msg);
		MyMessage(string message);
};

/* Custom class implementation for storing transaction info that will be used in MP2Node*/
struct transaction {
    public:
    int gtransID;
    int localTimeStamp;
    int qc;
    MessageType trans_type;
    string key;
    pair<int,string> latest_val;
    transaction(int tid, int lts, int qc, MessageType ttype,string k,string value):
			gtransID(tid), localTimeStamp(lts), qc(qc), trans_type(ttype), key(k), latest_val(0,value) { } 
};

/* Custom class implementations that will be used in MP2Node*/
class MP2Node {
private:
	// Vector holding the next two neighbors in the ring who have my replicas
	vector<Node> hasMyReplicas;
	// Vector holding the previous two neighbors in the ring whose replicas I have
	vector<Node> haveReplicasOf;
	// Ring
	vector<Node> ring;
	// Hash Table
	HashTable * ht;
	// Member representing this member
	Member *memberNode;
	// Params object
	Params *par;
	// Object of EmulNet
	EmulNet * emulNet;
	// Object of Log
	Log * log;

	// RAJA Code ends
    list<transaction> translog;
    map<string, Entry> RLocalHashTable;
    bool intialInit ;
    void processReadReply(Message message);
    void processReply(Message message);
    void sendMessage(MyMessage message, Address& toaddr);
    void updateTransactionLog();
    void processReplicate(Node toNode, ReplicaType rType);
	//RAJA Code ends

public:
	MP2Node(Member *memberNode, Params *par, EmulNet *emulNet, Log *log, Address *addressOfMember);
	Member * getMemberNode() {
		return this->memberNode;
	}

	// ring functionalities
	void updateRing();
	vector<Node> getMembershipList();
	size_t hashFunction(string key);
	void findNeighbors();

	// client side CRUD APIs
	void clientCreate(string key, string value);
	void clientRead(string key);
	void clientUpdate(string key, string value);
	void clientDelete(string key);

	// receive messages from Emulnet
	bool recvLoop();
	static int enqueueWrapper(void *env, char *buff, int size);

	// handle messages from receiving queue
	void checkMessages();

	// coordinator dispatches messages to corresponding nodes
	void dispatchMessages(MyMessage message);

	// find the addresses of nodes that are responsible for a key
	vector<Node> findNodes(string key);

	// server
	bool createKeyValue(string key, string value, ReplicaType replica);
	string readKey(string key);
	bool updateKeyValue(string key, string value, ReplicaType replica);
	bool deletekey(string key);

	// stabilization protocol - handle multiple failures
	void stabilizationProtocol();

	~MP2Node();
};

#endif /* MP2NODE_H_ */
