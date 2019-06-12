pragma solidity >=0.4.24;      //using 0.4.24
pragma experimental ABIEncoderV2;
// node deploy.js

// 

contract Voting{
    
    uint private quorum; // max quorum
    uint curr_quorum; // to count the current quorum from 0 to max quorum
    
    address private ChairCreator; // creator address
    
    constructor(uint _quorum) public{      //initial the quorum 
        quorum = _quorum;                  //and set the ChairCreator to sender address
        ChairCreator = msg.sender;
        curr_quorum = 0;
    }
    

    struct Voter{                           //Voter struct 
        string name;
        bool voted; // if true, then the person already voted
    }
    
    struct Proposal{                        //Proposal struct 
        string name; // short name(string type)
        uint voteCount; // the total number of accumulated votes
    }
    
    Proposal[] public proposals; // dynamically array of Proposal struct
    Voter[] public voters; // dynamically array of voter struct

    function addChoice(string _name) public{            //add choices
        require(ChairCreator == msg.sender);            // only creator can do this function
        
        proposals.push(Proposal({                       //push in the array
                name: _name,
                voteCount: 0
            }));
    }
    function addFriends(string _name) public{           // add friends
        require(ChairCreator == msg.sender);            // only creator can do this function
        voters.push(Voter({
                name: _name,
                voted: false
            }));
    }

    function voteTo(string voteFrom, string _voteTo) public returns(string){ //friends vote to proposal
        require(                                                             // only creator can do this function 
            (msg.sender == ChairCreator)&& (quorum > curr_quorum),          // quorum > curr_quorum or cannot vote more
            "It meets the max quorum"
            );
        for(uint i = 0; i< voters.length;i++){                              // in voters array to find the name voteFrom and it also need to not voted before
            if(keccak256(abi.encodePacked(voters[i].name)) == keccak256(abi.encodePacked(voteFrom))
            && !voters[i].voted){
                for(uint j; j<proposals.length;j++){                        // in proposal array to find the name voteTo
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