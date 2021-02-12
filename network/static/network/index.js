document.addEventListener('DOMContentLoaded', function(){
	
	if (document.querySelector('#newpost')) {
		document.querySelector('#newpost-form').addEventListener('submit',()=>create_post());
	}
	
	
	document.querySelectorAll('.edit-button').forEach(button =>{
		
		button.onclick=function(){
			
			const id =this.dataset.id;
			create_editform(id);
		

		}
		
	});

	document.querySelectorAll('.like-button').forEach(button =>{
		
		button.onclick=function(){
			
			const id =this.dataset.id;
			const post=document.getElementById(id);
			const children=post.children;
		    const grand_children=children[1].children;
		    const likes=grand_children[2].children[0].innerHTML;
			like(id,likes);
		

		}
		
	});

});

function like(id,likes){
	event.preventDefault();
	fetch('/like',{
		method:'PUT',
		body:JSON.stringify({
			id:id})
	})
	.then(res=>res.json())
	.then(result=>{
		if ("error" in result) {
      alert(`${result.error}`);
      }
      else{
      	
      	const post=document.getElementById(id);
      	post.scrollIntoView();

      		
		const children=post.children;
		const grand_children=children[1].children;
		if (likes > result.likes) {
			grand_children[2].children[0].innerHTML= result.likes ;
			grand_children[2].children[1].innerHTML= "Like" ;
		}
		else{
		grand_children[2].children[0].innerHTML= result.likes ;
		grand_children[2].children[1].innerHTML= "Unlike" ;
		}

    }

	});


}



function create_post(){
	
	const post=document.querySelector('#newpost-textarea').value;
	
	fetch('/newpost',{
		method:'POST',
		body: JSON.stringify({
			post:post})
	})
	.then(res=>res.json())
	.then(result=> {

		if ("error" in result) {
      alert(`${result.error}`);
      }
      else{
      document.querySelector('#newpost-textarea').value='';
        
      add_post(result.id,result.user,result.content,result.date,result.likes);
  }
        	
        
	});
	
	return false;
};

function add_post(id,user,content,date,likes){

	    	const div_card= document.createElement('div');
			const h5=document.createElement('h5');
			const card_body=document.createElement('div');
			const h51=document.createElement('h5');
			const p=document.createElement('p');
			const button = document.createElement('button');
			const posts_div=document.querySelector('#posts');
			const a =document.createElement('a');
			const edit_button=document.createElement('button');
			
			div_card.className='card';
			div_card.style.margin = 'auto';
			div_card.style.width = '90%';
			div_card.id=id;
			
			edit_button.className="edit-button";
			edit_button.style.float="right";
			edit_button.dataset.id=id;
			edit_button.innerHTML="Edit";

			h5.className='card-header';
			card_body.className='card-body';
			h51.className='card-title';
			p.className='card-text';
			button.className='like-button';
			a.href=`/profile/${user}`;

			edit_button.addEventListener('click',()=> create_editform(id));
			
			h5.innerHTML=user;
			h51.innerHTML=content;
			p.innerHTML=date;
			button.innerHTML=`${likes}  Likes`;
			
			card_body.appendChild(h51);
			card_body.appendChild(p);
			card_body.appendChild(button);
			card_body.appendChild(edit_button);
			a.appendChild(h5);
			div_card.appendChild(a);
			div_card.appendChild(card_body);
			posts_div.prepend(div_card);

			

			}

function edit(id){
	event.preventDefault();
	const new_post=document.getElementById('textarea').value;
	fetch('/edit', {
      method: 'PUT',
      body: JSON.stringify({
      content: new_post,
      id:id
      })

    })
    .then(response => response.json())
    .then(result => {

    	if ("error" in result) {
      		alert(`${result.error}`);
      	}
      	else{
      		
      		const post=document.getElementById(id);
      		post.scrollIntoView();

      		
			const children=post.children;
			const grand_children=children[1].children;
			grand_children[0].innerHTML=result.content;
			grand_children[0].style.display='initial';
			grand_children[2].innerHTML=result.date;
			grand_children[1].remove();
			grand_children[3].style.display="none";
      	}


	});
	
}

function create_editform(id){
			
			
			post=document.getElementById(id);
			post.scrollIntoView();

			const children=post.children;
			const grand_children=children[1].children;
			const content=grand_children[0].innerHTML;
			grand_children[0].style.display='none';
			const form=document.createElement('form');
			const textarea=document.createElement('textarea');
			const save_edit=document.createElement('input');

			const cancel=grand_children[3];
			cancel.style.display="block";
			
			
				
			//form.method="PUT";
			save_edit.type="submit";
			save_edit.value="Save Edit";
			
			textarea.style.display='block';
			textarea.style.width= '90%' ;
			textarea.style.margin='auto';
			textarea.id="textarea";

			
			textarea.innerHTML=content;
			form.appendChild(textarea);
			form.appendChild(save_edit);
			children[1].insertBefore(form,grand_children[1]);


			cancel.onclick=function(){
				form.remove();
				cancel.style.display="none";
				grand_children[0].style.display='block';
				
			};
			form.addEventListener('submit', ()=> edit(id))

}





