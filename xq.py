import os
import sys
from colorama import Style, Fore, init


class Template:
    def __init__(self):
        pass


logo = f"""              


          ;$&&&&&&$X                    
        &&&&&&&&&&&&&&x                 
       .&&&&&&&&&&&&&&   :              
       $&&&&&&&&&&&&&&   &&&&X     ;&&& 
       &&&&&&&&&&&&&&   &&&&&&&&&&&&&&X 
      &&&&&&&&&&&&&&+  :&&&&&&&&&&&&&&  
     ;&&&&&&&&&&&&&&   &&&&&&&&&&&&&&$  
     $;         :&&X  :&&&&&&&&&&&&&&   
          ++          &&&&&&&&&&&&&&x   
    &&&&&&&&&&&&&+    $&&&&&&&&&&&&&    
   x&&&&&&&&&&&&&&        .X&X;         
   &&&&&&&&&&&&&&:  X&&;         .X     
  X&&&&&&&&&&&&&&   &&&&&&&&&&&&&&;     
  &&&&&&&&&&&&&&:  x&&&&&&&&&&&&&&      
 X&&&&&&&&&&&&&&   &&&&&&&&&&&&&&       
 &&&&x: .x&&&&&   &&&&&&&&&&&&&&$         {Style.DIM}{Fore.BLACK}██{Fore.RED}██{Fore.GREEN}██{Fore.YELLOW}██{Fore.BLUE}██{Fore.MAGENTA}██{Fore.CYAN}██{Fore.WHITE}██{Style.RESET_ALL}
              x   &&&&&&&&&&&&&&.         {Fore.BLACK}██{Style.RESET_ALL}{Fore.RED}██{Style.RESET_ALL}{Fore.GREEN}██{Style.RESET_ALL}{Fore.YELLOW}██{Style.RESET_ALL}{Fore.BLUE}██{Style.RESET_ALL}{Fore.MAGENTA}██{Style.RESET_ALL}{Fore.CYAN}██{Style.RESET_ALL}{Fore.WHITE}██{Style.RESET_ALL}
                 +&&&&&&&&&&&&&&          {Style.BRIGHT}{Fore.BLACK}██{Fore.RED}██{Fore.GREEN}██{Fore.YELLOW}██{Fore.BLUE}██{Fore.MAGENTA}██{Fore.CYAN}██{Fore.WHITE}██{Style.RESET_ALL}
                    X&&&&&&&$
                    
                    
                    """

if __name__ == "__main__":
    print(logo)
