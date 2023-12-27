import uiautomator2 as u2
import time, os
from multiprocessing import Process


################################################################################################################################################################
#######################################################____File Handling____####################################################################################

def get_comments_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            comments = file.readlines()
            return [comment.strip() for comment in comments if comment.strip()]  # Remove empty lines and whitespace
    except Exception as e:
        print(f"Error reading comments from file: {e}")
        return []



saved_captions = set()  # Initialize a set to store saved captions

def save_captions_to_file(captions):
    global saved_captions
    try:
        with open('captions.txt', 'a', encoding='utf-8') as file:
            if captions not in saved_captions:
                file.write(captions + '\n\n')
                file.write("##############################################################################\n")
                file.write("##############################################################################\n")
                saved_captions.add(captions)  # Add the caption to the set of saved captions
    except Exception as e:
        print(f"Error saving captions to file: {e}")




def read_device_ips_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            devices = [line.strip() for line in file.readlines()]
            return devices
    except Exception as e:
        print(f"Error reading device IPs from file: {e}")
        return []

################################################################################################################################################################
#######################################################____File Handling____####################################################################################
def check_keywords(device_ip):
    device = u2.connect(device_ip)
    device.session("com.instagram.android")
    device.sleep(4)

    searchButton = device.xpath('//*[@resource-id="com.instagram.android:id/search_tab"]')
    searchButton.click()
    device.sleep(2)
    
    searchBar = device.xpath('//*[@resource-id="com.instagram.android:id/action_bar_search_hints_text_layout"]')
    searchBar.set_text("#giveaway")
    
    seeAllResults = device(text="See all results")
    seeAllResults.click()
    time.sleep(2)

    # Click on the element with text "Tags"
    tagsElement = device.xpath('//*[@text="Tags"]')
    tagsElement.click()
    time.sleep(2)


  
    element = device.xpath('//*[@resource-id="com.instagram.android:id/recycler_view"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]')
    element.click()
    time.sleep(4)


###############################################################################################################################################
###############################################################################################################################################

def action(device_ip):
    print("[+]Bot Started")
    while True:
        check_keywords(device_ip)
        device = u2.connect(device_ip)

        post_index = 1
        loop_count = 0
        total_loops = 0
        while total_loops < 60:
            # Assuming the posts are accessible via some kind of list or container
            print(f"[+]Clicked on the post {post_index}")
            post = device(resourceId="com.instagram.android:id/image_button", index=post_index)

            # Check if the post exists, if not, exit the loop
            if not post.exists:
                    # device.swipe_ext("up", steps=20)
                    continue   

            post.click()


            time.sleep(1)
            try:
                device.swipe_ext("up", steps=10)
                likeButton = device(resourceId="com.instagram.android:id/row_feed_button_like")
                likeButton.click()
                print("[+]Liked the post")
                more = device.xpath('//*[@content-desc="more"]')
                if more.exists:
                    more.click()
                        

                time.sleep(1)
                
                # device.swipe_ext("up", steps=20) 

                caption = device(resourceId="com.instagram.android:id/row_feed_comment_textview_layout")
                # caption.click()

                if caption.exists():
                    caption_text = caption.get_text()
                    # print("Caption:", caption_text)
                    save_captions_to_file(caption_text)
                    print("[+]Caption Saved")
            except:
                pass

            commentButton = device(resourceId="com.instagram.android:id/row_feed_button_comment")
            commentButton.click()

            try:
                comments = get_comments_from_file("comments.txt")
                for comment_text in comments:
                    try:
                        comment = device(resourceId="com.instagram.android:id/layout_comment_thread_edittext")
                        comment.set_text(comment_text)

                        commentPost = device(resourceId="com.instagram.android:id/layout_comment_thread_post_button_icon")
                        commentPost.click()
                        print("[+]Commented on the Post")
                        print("\n*****************************************************\n\n")
                        time.sleep(2)
                        device.press('back')
                    except Exception as e:
                        print(f"Error commenting: {e}")
                        pass
            except Exception as e:
                print(f"Error while processing comments: {e}")
                pass
                
            time.sleep(1)
            device.press('back')

            time.sleep(120)
            device.press('back')
            post_index += 1

            loop_count += 1

            if loop_count == 9:
                    device.swipe_ext("up", steps=50) 
                    device.swipe_ext("up", steps=50) 
                    time.sleep(2)
                    loop_count = 0
                    post_index = 1
                    post = device(resourceId="com.instagram.android:id/image_button", index=post_index)
                    post.click()
                    device.press('back')
                    post_index = 6
            

            time.sleep(3)
            total_loops += 1

        print("\n\n\nTaking a break for 12 hours...")
        time.sleep(12*60*60)  # Sleep for 12 hours
        total_loops = 0  # Reset loop count after the break

###############################################################################################################################################
###############################################################################################################################################


def run_instagram_interaction(device_ip):
    try:
        action(device_ip)
    except Exception as e:
        print(f"Error with {device_ip}: {e}")  






###############################################################################################################################################
###############################################################################################################################################

def main():
    devices = read_device_ips_from_file("devices.txt")

    processes = [Process(target=run_instagram_interaction, args=(device,)) for device in devices]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

if __name__ == "__main__":
    main()