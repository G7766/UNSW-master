pragma solidity >=0.4.24;      //using 0.4.24
pragma experimental ABIEncoderV2;
// node deploy.js


//name: PEIGUO GUAN 
//zID: z5143964
// metamask address: 0x3454e51FE8e2c4BD33d49ED4EEE5D385Ecc56537
// from : 0x3454e51fe8e2c4bd33d49ed4eee5d385ecc56537
// transaction hash: 0xda579d24607c96bccdb6c1a126a3a7e37ae041b3009e34b682f5dcec913dd218
/*
Test description: 1.using 0.4.24 to compile the code and run in JavaScriot VM
                  2.input the quorum number and deploy
                  3.the deploy account is creator account and only the creator can add choices, add friends,and
                    give other right to vote. creator has 1 chance to vote
                  4.using different (friedns') address as input to add friedns if friends account get the right,
                    need to change to friends account address and it has right to vote once.
                  5. voteTo input the name of choices" "aaa" " string types
                  6. Both of the creator and friends can using the getResult function to show the result
                  7. destruct function is to destroy the address so as to destroy the contract (But i worried if it is what the questions want)
The logic of my thinking and some details like function defination and variables are added in the code as comment.
*/
contract Voting{
    
    uint private quorum; // max quorum
    uint curr_quorum; // to count the current quorum from 0 to max quorum
    bool voted; // creator has one chance to vote
    uint weight; //creator has 1 chance to vote
    
    address private ChairCreator; // creator address
    
    constructor(uint _quorum) public{      //initial the quorum 
        quorum = _quorum;                  //and set the ChairCreator to sender address
        ChairCreator = msg.sender;
        curr_quorum = 0;
        voted = false; 
        weight = 1;
    }
    

    struct Voter{                           //Voter struct 
        //string name;
        bool voted; // if true, then the person already voted
        uint weight; //the right to vote, 0 for no right, 1 for have right
        //address voteraddress; // create voter addrress
    }
    
    struct Proposal{                        //Proposal struct 
        string name; // short name(string type)
        uint voteCount; // the total number of accumulated votes
    }
    
    Proposal[] public proposals; // dynamically array of Proposal struct
    //Voter[] public voters; // dynamically array of voter struct
    mapping(address => Voter) public voters;  // give all the voter an address
    
    function addChoice(string _name) public{            //add choices
        require(ChairCreator == msg.sender);            // only creator can do this function
        
        proposals.push(Proposal({                       //push in the array
                name: _name,
                voteCount: 0
            }));
    }
    function addFriends(address voter_address) public returns(string) {           // add friends
        require(ChairCreator == msg.sender,"Only creator has right to add friends");            // only creator can do this function
        voters[voter_address].voted = false;
        voters[voter_address].weight = 0;       // they have not right to vote until creator give them right "1"
        return "create friedns success";
    }
    
    function VoteTo(string _voteTo)public returns(string){     //Creator can vote once
        Voter storage sender = voters[msg.sender];
        require(                                                             
            (quorum > curr_quorum) &&!sender.voted && (sender.weight ==1),          
            "Voter has already voted or it meets the max quorum!"
            );
        for(uint j=0; j<proposals.length;j++){                        // in proposal array to find the name voteTo
            if(keccak256(abi.encodePacked(proposals[j].name)) == keccak256(abi.encodePacked(_voteTo))){
                proposals[j].voteCount = proposals[j].voteCount + 1;
                curr_quorum ++;                                     // curr_quorum ++ until up to quorum
                sender.weight =0;                                   // after voting they have not chance to vote again
                return "Votiing success!";                          // vote success return the word
                }
            }
        return "Creator has already voted or there is not this voter or proposal"; 
    }
    
    function GiveRightTovote(address voteraddress) public{ //give right to votor, give them 1 chance to vote
        require(
            (msg.sender == ChairCreator)&&(!voters[voteraddress].voted)&&(voters[voteraddress].weight==0)
            ,"you have not right to vote or you already vote!"
            );
            voters[voteraddress].weight = 1;   //give them 1 chance to vote
    }
    /*
    function voteto(string voteFrom, string _voteTo) public returns(string){ //friends vote to proposal
        require(                                                             // only creator can do this function 
            (msg.sender == ChairCreator)&& (quorum > curr_quorum),          // quorum > curr_quorum or cannot vote more
            "It meets the max quorum"
            );
        for(uint i = 0; i< voters.length;i++){                              // in voters array to find the name voteFrom and it also need to not voted before
            if(keccak256(abi.encodePacked(voters[i].name)) == keccak256(abi.encodePacked(voteFrom))
            && !voters[i].voted){
                for(uint j=0; j<proposals.length;j++){                        // in proposal array to find the name voteTo
                    if(keccak256(abi.encodePacked(proposals[j].name)) == keccak256(abi.encodePacked(_voteTo))){
                        proposals[j].voteCount = proposals[j].voteCount + 1;
                        voters[i].voted = true;                             // friedn has voted and set the voted to true
                        curr_quorum ++;                                     // curr_quorum ++ until up to quorum
                        return "Votiing success!";                          // vote success return the word
                    }
                }
            }
        }
        return "The voter has already voted or there is not this voter or proposal"; // if go to this step it means vote fail(because no name in voters array or proposals or the voter have voted)
    }
    
    
    function showAllVoters() external view returns(string[] memory name,bool[] memory voted ){ //this function to show the state of voters array
        name = new string[](voters.length);
        voted = new bool[](voters.length);
        for(uint i=0;i<voters.length;i++){                                                      //create memory value and put array value into it
           name[i]= voters[i].name;
           voted[i] = voters[i].voted;
        }
    }
    */
    
    function getResult() external view returns(string[] memory name,uint[] memory count ){  // this function to show the result and everyone can use this
        name = new string[](proposals.length);
        count = new uint[](proposals.length);
        for(uint i=0;i<proposals.length;i++){                                               //create memory value and put array value into it
           name[i]= proposals[i].name;
           count[i] = proposals[i].voteCount;
        }
    }
    
    function destruct() public{                 // destroy the contract by selfdestruct the address
        require(
            ChairCreator == msg.sender,
            "Only the Creator can destroy the contract");
        selfdestruct(ChairCreator);
    }
    
    
}