/**********************************
 * FILE NAME: MP1Node.cpp
 *
 * DESCRIPTION: Membership protocol run by this Node.
 * 				Definition of MP1Node class functions.
 **********************************/

#include "MP1Node.h"
#include <arpa/inet.h>

using namespace std;
/*
 * Note: You can change/add any functions in MP1Node.{h,cpp}
 */

/**
 * Overloaded Constructor of the MP1Node class
 * You can add new members to the class if you think it
 * is necessary for your logic to work
 */
MP1Node::MP1Node(Member *member, Params *params, EmulNet *emul, Log *log, Address *address) {
	for( int i = 0; i < 6; i++ ) {
		NULLADDR[i] = 0;
	}
	this->memberNode = member;
	this->emulNet = emul;
	this->log = log;
	this->par = params;
	this->memberNode->addr = *address;
#ifdef DEBUGLOG2
        log->LOG(address, "init function");
#endif
}

/**
 * Destructor of the MP1Node class
 */
MP1Node::~MP1Node() {}

/**
 * FUNCTION NAME: recvLoop
 *
 * DESCRIPTION: This function receives message from the network and pushes into the queue
 * 				This function is called by a node to receive messages currently waiting for it
 */
int MP1Node::recvLoop() {
    if ( memberNode->bFailed ) {
    	return false;
    }
    else {
    	return emulNet->ENrecv(&(memberNode->addr), enqueueWrapper, NULL, 1, &(memberNode->mp1q));
    }
}

/**
 * FUNCTION NAME: enqueueWrapper
 *
 * DESCRIPTION: Enqueue the message from Emulnet into the queue
 */
int MP1Node::enqueueWrapper(void *env, char *buff, int size) {
	Queue q;
	return q.enqueue((queue<q_elt> *)env, (void *)buff, size);
}

/**
 * FUNCTION NAME: nodeStart
 *
 * DESCRIPTION: This function bootstraps the node
 * 				All initializations routines for a member.
 * 				Called by the application layer.
 */
void MP1Node::nodeStart(char *servaddrstr, short servport) {
    Address joinaddr;
    joinaddr = getJoinAddress();

    // Self booting routines
    if( initThisNode(&joinaddr) == -1 ) {
#ifdef DEBUGLOG
        log->LOG(&memberNode->addr, "init_thisnode failed. Exit.");
#endif
        exit(1);
    }

    if( !introduceSelfToGroup(&joinaddr) ) {
        finishUpThisNode();
#ifdef DEBUGLOG
        log->LOG(&memberNode->addr, "Unable to join self to group. Exiting.");
#endif
        exit(1);
    }

    return;
}

/**
 * FUNCTION NAME: initThisNode
 *
 * DESCRIPTION: Find out who I am and start up
 */
//join addr is 1.0.0.0:0
int MP1Node::initThisNode(Address *joinaddr) {
	/*
	 * This function is partially implemented and may require changes
	 */
	int id = *(int*)(&memberNode->addr.addr);
	int port = *(short*)(&memberNode->addr.addr[4]);

	memberNode->bFailed = false;
	memberNode->inited = true;
	memberNode->inGroup = false;
    // node is up!
	memberNode->nnb = 0;
	memberNode->heartbeat = 0;
	memberNode->pingCounter = TFAIL;
	memberNode->timeOutCounter = -1;
    initMemberListTable(memberNode);

    return 0;
}

/**
 * FUNCTION NAME: introduceSelfToGroup
 *
 * DESCRIPTION: Join the distributed system
 */
int MP1Node::introduceSelfToGroup(Address *joinaddr) {
	MessageHdr *msg;
#ifdef DEBUGLOG
    static char s[1024];
#endif

    if ( 0 == memcmp((char *)&(memberNode->addr.addr), (char *)&(joinaddr->addr), sizeof(memberNode->addr.addr))) {
        // I am the group booter (first process to join the group). Boot up the group
#ifdef DEBUGLOG
        log->LOG(&memberNode->addr, "Starting up group...");
#endif
        memberNode->inGroup = true;
    }
    else {
        size_t msgsize = sizeof(MessageHdr) + sizeof(joinaddr->addr) + sizeof(long) + 1;
        msg = (MessageHdr *) malloc(msgsize * sizeof(char));

        // create JOINREQ message: format of data is {struct Address myaddr} RAJA
        msg->msgType = JOINREQ;
        memcpy((char *)(msg+1), &memberNode->addr.addr, sizeof(memberNode->addr.addr));
        memcpy((char *)(msg+1) + 1 + sizeof(memberNode->addr.addr), &memberNode->heartbeat, sizeof(long));
#ifdef DEBUGLOG2
        log->LOG(&memberNode->addr, "heartbeat: %d", &memberNode->heartbeat);
#endif

#ifdef DEBUGLOG
        sprintf(s, "Trying to join...");
        log->LOG(&memberNode->addr, s);
#endif

        // send JOINREQ message to introducer member
        emulNet->ENsend(&memberNode->addr, joinaddr, (char *)msg, msgsize);

        free(msg);
    }

    return 1;

}

/**
 * FUNCTION NAME: finishUpThisNode
 *
 * DESCRIPTION: Wind up this node and clean up state
 */
int MP1Node::finishUpThisNode(){
   /*
    * Your code goes here
    */
}

/**
 * FUNCTION NAME: nodeLoop
 *
 * DESCRIPTION: Executed periodically at each member
 * 				Check your messages in queue and perform membership protocol duties
 */
void MP1Node::nodeLoop() {
    if (memberNode->bFailed) {
    	return;
    }

    // Check my messages
    checkMessages();

    // Wait until you're in the group...
    if( !memberNode->inGroup ) {
    	return;
    }

    // ...then jump in and share your responsibilites!
    nodeLoopOps();

    return;
}

/**
 * FUNCTION NAME: checkMessages
 *
 * DESCRIPTION: Check messages in the queue and call the respective message handler
 */
void MP1Node::checkMessages() {
    void *ptr;
    int size;

    // Pop waiting messages from memberNode's mp1q
    while ( !memberNode->mp1q.empty() ) {
    	ptr = memberNode->mp1q.front().elt;
    	size = memberNode->mp1q.front().size;
    	memberNode->mp1q.pop();
    	recvCallBack((void *)memberNode, (char *)ptr, size);
    }
    return;
}

/**
 * FUNCTION NAME: recvCallBack
 *
 * DESCRIPTION: Message handler for different message types
 */
/**
 * Message Types
 enum MsgTypes{
    JOINREQ,
    JOINREP,
    HEARBEAT,
    DUMMYLASTMSGTYPE
};
*/
bool MP1Node::recvCallBack(void *env, char *data, int size ) {
	/*
	 * Your code goes here
	 */
    MessageHdr *rxMsg = (MessageHdr *)data;
    if(rxMsg->msgType == MsgTypes::JOINREQ) {
        //add new member to the member list
        addMember(rxMsg);
        //make a JOINResp
        sendJoinResponse();
        cout << "send [" << par->getcurrtime() << "] JOINREP [" << memberNode->addr.getAddress() << "] to " << rxMsg->addr.getAddress() << endl;
    } else if (rxMsg->msgType == MsgTypes::JOINREP) {
        // add to group
        memberNode->inGroup = true;
        // add member to list
        addMember(rxMsg);
        cout << "receive [" << par->getcurrtime() << "]  JOINREP [" << memberNode->addr.getAddress() << "] from " << rxMsg->addr.getAddress() << endl;
    } else if (rxMsg->msgType == MsgTypes::HEARBEAT) {
        // 1. find the member and increment heartbeat
        // 2. if doesn't exist add the member
        cout << "received HeartBeat Message " << endl;

    } else {
 #ifdef DEBUGLOG2 
    log->LOG(&memberNode->addr, "something went wrong. this message type shouldn't come");
#endif       
    }
    // who deletes rxMsg??
}

void MP1Node::sendJoinResponse() {
    MessageHdr *resp = new MessageHdr();
    resp->msgType = MsgTypes::JOINREP;
    memcpy(&resp->addr, &memberNode->addr, sizeof(Address));
    resp->memberListCnt = memberNode->memberList.size();
    //copy memberlist;
    if(resp->memberListCnt > 0) {
        resp->memberList = new MemberListEntry[resp->memberListCnt];
        memcpy(resp->memberList, memberNode->memberList.data(), sizeof(MemberListEntry) * resp->memberListCnt);
    }    
    emulNet->ENsend(&memberNode->addr, &resp->addr, (char *)resp, sizeof(MessageHdr));
    // who deletes *resp?
    delete resp;
}

void MP1Node::sendHeatBeat() {
    MessageHdr *heartbeat = new MessageHdr();
    heartbeat->msgType = MsgTypes::HEARBEAT;
    memcpy(&heartbeat->addr, &memberNode->addr, sizeof(Address));
    heartbeat->memberListCnt = memberNode->memberList.size();

    if(heartbeat->memberListCnt > 0) {
        heartbeat->memberList = new MemberListEntry[heartbeat->memberListCnt];
        memcpy(heartbeat->memberList, memberNode->memberList.data(), sizeof(MemberListEntry) * heartbeat->memberListCnt);
    }

    for(int i = 0; i < memberNode->memberList.size(); i++) {
        MemberListEntry *temp = memberNode->memberList.data();
        Address *tempAddr = new Address();
        memcpy(tempAddr->addr, &temp->id, sizeof(int));
        memcpy(tempAddr->addr + sizeof(int), &temp->port, sizeof(short));
        emulNet->ENsend(&memberNode->addr, tempAddr, (char *) heartbeat, sizeof(MessageHdr));
        delete tempAddr;
    }
    delete heartbeat;
}

void MP1Node::addMember(MessageHdr *msg) {
    int id = 0;
    short port;
    memcpy(&id, &msg->addr.addr[0], sizeof(int));
    memcpy(&port, &msg->addr.addr[4], sizeof(short));

    int msgid = *(int*)(&msg->addr.addr);
    short msgport = *(short*)(&msg->addr.addr[4]);

    if( id != msgid || port != msgport) 
        cout << "RAJA Bug BUG BUG!!" << endl;

    for(int i = 0; i < memberNode->memberList.size(); i++) {
        MemberListEntry *temp = memberNode->memberList.data();
        if(temp->getid() == id && temp->getport() == port) {
            // already a member;
            return;
        }
    }
    //add to memberList
    MemberListEntry *memb = new MemberListEntry(id, port, 1, par->getcurrtime());
    memberNode->memberList.push_back(*memb);

    //log it
    log->logNodeAdd(&memberNode->addr, &msg->addr);
    return;
}

/**
 * FUNCTION NAME: nodeLoopOps
 *
 * DESCRIPTION: Check if any node hasn't responded within a timeout period and then delete
 * 				the nodes
 * 				Propagate your membership list
 */
void MP1Node::nodeLoopOps() {

	/*
	 * Your code goes here
	 */
    // remove members whose time stamp difference is over TREMOVE\
    
    for(int i = 0; i < memberNode->memberList.size(); i++) {
        MemberListEntry temp = memberNode->memberList[i];
        if (par->getcurrtime() - temp.gettimestamp() >= TREMOVE) {
            // find temp in memberNode->memberList
            Address *delAddr =  new Address();
            memcpy(delAddr->addr, &temp.id, sizeof(int));
            memcpy(delAddr->addr + sizeof(int), &temp.port, sizeof(short));
            log->logNodeRemove(&memberNode->addr, delAddr);
            // remove this temp from memberNode->memberList
            vector<MemberListEntry>::iterator it = memberNode->memberList.begin();
            for(; it != memberNode->memberList.end(); it++) {
                MemberListEntry t = *it;
                if(t.id == temp.id && t.port == temp.port) {
                    it = memberNode->memberList.erase(it);
                    break;
                }
            }
        }
    }
    // now that the memberList is updated, send a heart beat message to everyone.


    return;
}

/**
 * FUNCTION NAME: isNullAddress
 *
 * DESCRIPTION: Function checks if the address is NULL
 */
int MP1Node::isNullAddress(Address *addr) {
	return (memcmp(addr->addr, NULLADDR, 6) == 0 ? 1 : 0);
}

/**
 * FUNCTION NAME: getJoinAddress
 *
 * DESCRIPTION: Returns the Address of the coordinator
 */
Address MP1Node::getJoinAddress() {
    Address joinaddr;

    memset(&joinaddr, 0, sizeof(Address));
    *(int *)(&joinaddr.addr) = 1;
    *(short *)(&joinaddr.addr[4]) = 0;

    return joinaddr;
}

/**
 * FUNCTION NAME: initMemberListTable
 *
 * DESCRIPTION: Initialize the membership list
 */
void MP1Node::initMemberListTable(Member *memberNode) {
	memberNode->memberList.clear();
}

/**
 * FUNCTION NAME: printAddress
 *
 * DESCRIPTION: Print the Address
 */
void MP1Node::printAddress(Address *addr)
{
    printf("%d.%d.%d.%d:%d \n",  addr->addr[0],addr->addr[1],addr->addr[2],
                                                       addr->addr[3], *(short*)&addr->addr[4]) ;    
}
